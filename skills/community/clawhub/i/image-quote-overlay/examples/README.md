# Example: Tạo ảnh quote cho LinkedIn

## Cách sử dụng

### Cơ bản (sử dụng cấu hình mặc định)
```bash
./scripts/create-overlay-image.sh "Quote text" output.png
```

### Tùy chỉnh cấu hình (inline)
```bash
PICS_DIR="/path/to/images" \
AUTHOR_NAME="Your Name" \
AUTHOR_ROLE="Your Role" \
AUTHOR_CONTACT="your-website.com" \
./scripts/create-overlay-image.sh "Quote text" output.png
```

### Sử dụng file cấu hình
```bash
# 1. Copy file cấu hình mẫu
cp config.example.sh ~/.image-quote-overlay-config.sh

# 2. Chỉnh sửa file cấu hình
nano ~/.image-quote-overlay-config.sh

# 3. Load cấu hình và chạy script
source ~/.image-quote-overlay-config.sh
./scripts/create-overlay-image.sh "Quote text" output.png
```

## Ví dụ thực tế

### LinkedIn (cấu hình mặc định)
```bash
./scripts/create-overlay-image.sh "Start your day with AI, not busywork." /tmp/openclaw/uploads/linkedin-morning.png
```

### Facebook (cấu hình mặc định)
```bash
./scripts/create-overlay-image.sh "AI không thay thế bạn. Người biết dùng AI sẽ thay thế bạn." /tmp/openclaw/uploads/facebook-noon.png
```

### WordPress (cấu hình mặc định)
```bash
./scripts/create-overlay-image.sh "Tối ưu hoá chiến lược 3A: Từ Social sang Automation" /tmp/openclaw/uploads/wordpress-daily.png
```

### Tùy chỉnh cho người dùng khác
```bash
PICS_DIR="/Users/john/photos" \
AUTHOR_NAME="John Doe" \
AUTHOR_ROLE="Marketing Director" \
AUTHOR_CONTACT="john@example.com" \
./scripts/create-overlay-image.sh "Marketing is about telling stories." /tmp/openclaw/uploads/john-quote.png
```

### Tùy chỉnh cho người dùng khác (với file cấu hình)
```bash
# Tạo file cấu hình cho John
cat > ~/.john-quote-config.sh << 'EOF'
PICS_DIR="/Users/john/photos"
AUTHOR_NAME="John Doe"
AUTHOR_ROLE="Marketing Director"
AUTHOR_CONTACT="john@example.com"
EOF

# Load cấu hình và chạy script
source ~/.john-quote-config.sh
./scripts/create-overlay-image.sh "Marketing is about telling stories." /tmp/openclaw/uploads/john-quote.png
```

## Kết quả

Ảnh sẽ được tạo với:
- Kích thước: 1200x630px
- Gradient overlay từ trên trong suốt → dưới tối
- Quote text ở giữa
- Tên, vai trò, liên hệ ở dưới (theo cấu hình)

### Output example
```
Using photo: IMG_1234.JPG
Created: /tmp/openclaw/uploads/linkedin-morning.png
Photo used: IMG_1234.JPG
Author: QUOC MODORO
Role: CEO & FOUNDER — MODORO | YBAI
Contact: lebaoquoc.com
```

## Yêu cầu

- ImageMagick đã cài đặt (`magick` command)
- Font đã cài đặt:
  - Anton-Regular.ttf
  - Arial Bold.ttf
  - Arial.ttf
- Thư mục ảnh: PICS_DIR (chứa ảnh JPG)

## Workflow với skill khác

### LinkedIn Post
```bash
# 1. Tạo ảnh
source ~/.image-quote-overlay-config.sh
OUTPUT_PATH=$(./scripts/create-overlay-image.sh "Start your day with AI, not busywork." /tmp/openclaw/uploads/linkedin-morning.png | grep "Created:" | cut -d' ' -f2)

# 2. Sử dụng đường dẫn ảnh cho skill linkedin-post
# (skill linkedin-post sẽ upload ảnh và đăng bài)
```

### Facebook Post
```bash
# 1. Tạo ảnh
source ~/.image-quote-overlay-config.sh
OUTPUT_PATH=$(./scripts/create-overlay-image.sh "AI không thay thế bạn." /tmp/openclaw/uploads/facebook-noon.png | grep "Created:" | cut -d' ' -f2)

# 2. Sử dụng đường dẫn ảnh cho skill facebook-post
# (skill facebook-post sẽ upload ảnh và đăng bài)
```

### WordPress Post
```bash
# 1. Tạo ảnh
source ~/.image-quote-overlay-config.sh
OUTPUT_PATH=$(./scripts/create-overlay-image.sh "Tối ưu hoá chiến lược 3A" /tmp/openclaw/uploads/wordpress-daily.png | grep "Created:" | cut -d' ' -f2)

# 2. Sử dụng đường dẫn ảnh cho skill wordpress-post
# (skill wordpress-post sẽ upload ảnh và đăng bài)
```
