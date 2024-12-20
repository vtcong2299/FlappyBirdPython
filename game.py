import pygame, sys, random

# Tạo hàm cho trò chơi
def draw_floor():
    # Vẽ sàn lặp lại hai lần để tạo hiệu ứng cuộn
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))

def create_pipe():
    # Tạo ra cặp ống trên và dưới với khoảng cách ngẫu nhiên
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(500, random_pipe_pos - gap_size))
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    # Di chuyển các ống sang trái
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes

def draw_pipe(pipes):
    # Vẽ các ống lên màn hình
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    # Kiểm tra va chạm giữa chim và các ống hoặc ranh giới trên và dưới của màn hình
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True

def rotate_bird(bird1):
    # Quay chim dựa trên chuyển động của nó
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    # Thay đổi hình ảnh của chim để tạo hiệu ứng vỗ cánh
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    # Hiển thị điểm số lên màn hình
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 50))  # Giảm độ cao của high score thêm nữa
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    # Cập nhật điểm số cao nhất
    if score > high_score:
        high_score = score
    return high_score

def score_check():
    # Kiểm tra và tăng điểm số khi chim vượt qua một ống
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1  # Tăng điểm số lên 1 khi vượt qua ống
                can_score = False  # Đảm bảo không cộng điểm nhiều lần
                score_sound.play()                
            elif pipe.centerx < 0:  # Khi ống đã qua màn hình
                can_score = True  # Cho phép cộng điểm cho ống tiếp theo


# Khởi tạo Pygame và các biến trò chơi
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 35)

# Thiết lập các biến
gravity = 0.2  # Giảm trọng lực
bird_movement = 0
game_active = False
game_started = False
score = 0
high_score = 0
gap_size = 250  # Tăng khoảng cách giữa các ống
can_score = True

# Chèn background
bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

# Chèn sàn
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# Tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]  # 0 1 2
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))

# Tạo timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

# Tạo ống
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# Tạo timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200, 300, 400]

# Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216, 384))

# Chèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

# Vòng lặp chính của trò chơi
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_started:
                # Bắt đầu trò chơi khi nhấn phím SPACE lần đầu tiên
                game_started = True
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
            elif event.key == pygame.K_SPACE and game_active:
                # Chim bay lên khi nhấn phím SPACE trong khi trò chơi đang hoạt động
                bird_movement = 0
                bird_movement = -7  # Giảm lực nhảy thêm một chút
                flap_sound.play()
            elif event.key == pygame.K_SPACE and not game_active:
                # Khởi động lại trò chơi khi nhấn phím SPACE sau khi trò chơi kết thúc
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0

        if event.type == spawnpipe and game_started:
            pipe_list.extend(create_pipe())

        if event.type == birdflap and game_started:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    screen.blit(bg, (0, 0))

    if game_active:        
        # Chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score_check()  # Kiểm tra điểm số khi vượt qua ống
        score_display('main game')
    else:
        if game_started:
            screen.blit(game_over_surface, game_over_rect)
            high_score = update_score(score, high_score)
            score_display('game_over')

    # Sàn
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
