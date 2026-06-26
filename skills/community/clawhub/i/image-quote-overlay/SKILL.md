# Image Quote Overlay Skill

## Mô tả
Tạo ảnh overlay quote từ ảnh cá nhân ngẫu nhiên với gradient và text. Hỗ trợ nhiều kích thước cho LinkedIn, X, Facebook, WordPress.

**Workflow**:
1. Người dùng cung cấp cấu hình (thư mục ảnh, tên tác giả, vai trò, liên hệ)
2. Gọi skill tạo ảnh với quote text
3. Skill tự lấy ảnh ngẫu nhiên từ thư mục
4. Tự động thiết kế hình với gradient overlay
5. Gửi hình + đường dẫn lại cho người dùng
6. Các skill khác có thể sử dụng đường dẫn ảnh

## Khi nào dùng skill này
- Cần tạo ảnh quote cho bài đăng LinkedIn, X, Facebook, WordPress
- Cần tạo ảnh với gradient overlay và text
- Cần tạo ảnh từ ảnh cá nhân ngẫu nhiên
- Cần tạo ảnh cho nhiều người dùng với cấu hình khác nhau

## Cấu hình

### Cấu hình mặc định
```bash
# Thư mục ảnh
PICS_DIR="/Users/quocmodoro/TinClaw/Pics"

# Tên tác giả
AUTHOR_NAME="QUOC MODORO"

# Vai trò
AUTHOR_ROLE="CEO & FOUNDER — MODORO | YBAI"

# Liên hệ
AUTHOR_CONTACT="lebaoquoc.com"
```

### Cấu hình tùy chỉnh
```bash
# Tạo file cấu hình
cat > ~/.image-quote-overlay-config.sh << 'EOF'
PICS_DIR="/path/to/your/images"
AUTHOR_NAME="Your Name"
AUTHOR_ROLE="Your Role"
AUTHOR_CONTACT="your-website.com"
EOF

# Sử dụng cấu hình
source ~/.image-quote-overlay-config.sh
./scripts/create-overlay-image.sh "Quote text" output.png
```

## Cách sử dụng

### Cơ bản
```bash
# Tạo ảnh với quote text (sử dụng cấu hình mặc định)
./scripts/create-overlay-image.sh "Quote text" output.png
```

### Tùy chỉnh cấu hình
```bash
# Tạo ảnh với cấu hình tùy chỉnh
PICS_DIR="/path/to/images" \
AUTHOR_NAME="Your Name" \
AUTHOR_ROLE="Your Role" \
AUTHOR_CONTACT="your-website.com" \
./scripts/create-overlay-image.sh "Quote text" output.png
```

### Ví dụ thực tế

#### LinkedIn
```bash
./scripts/create-overlay-image.sh "Start your day with AI, not busywork." /tmp/openclaw/uploads/linkedin-morning.png
```

#### Facebook
```bash
./scripts/create-overlay-image.sh "AI không thay thế bạn. Người biết dùng AI sẽ thay thế bạn." /tmp/openclaw/uploads/facebook-noon.png
```

#### WordPress
```bash
./scripts/create-overlay-image.sh "Tối ưu hoá chiến lược 3A: Từ Social sang Automation" /tmp/openclaw/uploads/wordpress-daily.png
```

#### Tùy chỉnh cho người dùng khác
```bash
PICS_DIR="/Users/john/photos" \
AUTHOR_NAME="John Doe" \
AUTHOR_ROLE="Marketing Director" \
AUTHOR_CONTACT="john@example.com" \
./scripts/create-overlay-image.sh "Marketing is about telling stories." /tmp/openclaw/uploads/john-quote.png
```

## Cấu trúc ảnh

### Kích thước
- **Mặc định**: 1200x630px (chuẩn LinkedIn, X, Facebook)
- **Lề**: 60px trái/phải
- **Quote box**: 1080px wide, 160px tall

### Layout (từ dưới lên)
- 36px: Liên hệ (website/email)
- 62px: Vai trò
- 100px: Tên tác giả
- 150px: quote box bottom edge

### Gradient
- Từ trên trong suốt → dưới tối (rgba(0,0,0,0.88))

## Yêu cầu hệ thống

### Phần mềm
- **ImageMagick**: `magick` command
- **Bash shell**

### Font
- **Anton-Regular.ttf**: `/Users/quocmodoro/Library/Fonts/Anton-Regular.ttf` (cho quote text)
- **Arial Bold.ttf**: `/System/Library/Fonts/Supplemental/Arial Bold.ttf` (cho tên)
- **Arial.ttf**: `/System/Library/Fonts/Supplemental/Arial.ttf` (cho subtitle)

### Thư mục ảnh
- **Định dạng**: JPG only (bỏ qua HEIC)
- **Số lượng**: Cần ít nhất 1 ảnh JPG

## Script

### Đường dẫn
`/Users/quocmodoro/.openclaw/workspace/skills/image-quote-overlay/scripts/create-overlay-image.sh`

### Quy trình
1. Random chọn 1 ảnh JPG từ thư mục (PICS_DIR)
2. Resize ảnh gốc về 1200px width
3. Crop center về 1200x630
4. Tạo gradient từ trên trong suốt → dưới tối
5. Tạo quote text box
6. Compose tất cả lại với layout từ bottom (tên, vai trò, liên hệ)
7. Cleanup temporary files
8. Trả về đường dẫn ảnh

## Output

### Đường dẫn ảnh
- Script trả về đường dẫn ảnh đã tạo
- Có thể dùng cho các skill khác (upload, đăng bài, v.v.)

### Ví dụ output
```
Created: /tmp/openclaw/uploads/linkedin-morning.png
Photo used: IMG_1234.JPG
```

## Lưu ý

### Font
- Nếu font không tồn tại, script sẽ báo lỗi
- Cần cài đặt font trước khi chạy script

### Ảnh
- Chỉ hỗ trợ JPG, không hỗ trợ HEIC
- Nếu không có ảnh JPG trong thư mục, script sẽ báo lỗi

### Cấu hình
- Có thể cấu hình qua environment variables
- Có thể tạo file cấu hình riêng cho từng người dùng

### Output
- Output mặc định: `/tmp/openclaw/uploads/overlay-output.png`
- Quality: 95%

## Troubleshooting

### Lỗi: No JPG files in directory
**Giải pháp**: Thêm ảnh JPG vào thư mục PICS_DIR

### Lỗi: Font not found
**Giải pháp**: Cài đặt font hoặc cập nhật đường dẫn font trong script

### Lỗi: magick command not found
**Giải pháp**: Cài đặt ImageMagick:
```bash
brew install imagemagick
```

### Lỗi: PICS_DIR not set
**Giải pháp**: Thiết lập PICS_DIR hoặc sử dụng cấu hình mặc định

## Tích hợp với OpenClaw

### Cron jobs
Skill này được dùng trong các cron jobs:
- LinkedIn Daily Content Draft (7:00)
- Facebook Draft (12:00)
- WordPress Post (11:00)

### Workflow
1. Tạo ảnh quote với script
2. Upload ảnh lên platform (LinkedIn, Facebook, WordPress)
3. Đăng bài với ảnh

### Tích hợp với skill khác
- **linkedin-post**: Tạo ảnh cho bài LinkedIn
- **facebook-post**: Tạo ảnh cho bài Facebook
- **wordpress-post**: Tạo ảnh cho bài WordPress
- **x-post**: Tạo ảnh cho bài X/Twitter

## Cập nhật
- **Ngày tạo**: 2026-04-30
- **Phiên bản**: 2.0
- **Trạng thái**: Đang hoạt động
- **Cập nhật**: Thêm cấu hình linh hoạt cho nhiều người dùng

## Tác giả
- Script gốc: Quoc MODORO
- Skill: Tin (OpenClaw Assistant)
