# Hướng dẫn lấy Preny Token

## Cách 1: Từ Browser DevTools

### Bước 1: Mở Preny Dashboard
Truy cập: https://app.preny.ai và đăng nhập

### Bước 2: Mở DevTools
- **Chrome/Edge**: Nhấn `F12` hoặc `Cmd+Option+I` (Mac)
- **Firefox**: Nhấn `F12` hoặc `Cmd+Shift+I` (Mac)
- **Safari**: Enable Developer menu trước: Preferences → Advanced → Show Develop menu

### Bước 3: Chuyển sang Tab Network
1. Click tab **Network** trong DevTools
2. Check option **Preserve log** (nếu có)
3. Thao tác bất kỳ trên dashboard (click vào thống kê, chuyển trang...)

### Bước 4: Tìm Request có Token
1. Trong danh sách requests, tìm request có tên `stats` hoặc `statistics`
2. Click vào request đó
3. Chuyển sang tab **Headers**
4. Tìm mục **Request Headers**
5. Tìm dòng `Authorization: Bearer <token>`
6. Copy phần token (chuỗi sau "Bearer ")

### Bước 5: Lưu Token
```bash
# Thêm vào environment
export PRENY_TOKEN="your-token-here"

# Hoặc thêm vào bashrc để dùng lâu dài
echo 'export PRENY_TOKEN="your-token-here"' >> ~/.bashrc
source ~/.bashrc
```

## Cách 2: Từ Console (Cách nhanh)

1. Mở DevTools (`F12`)
2. Chuyển sang tab **Console**
3. Paste đoạn code sau:

```javascript
// Lấy token từ localStorage
const token = localStorage.getItem('token') || 
              JSON.parse(localStorage.getItem('user') || '{}').token;
console.log('Your Preny Token:', token);
```

4. Copy token được in ra

## Token hết hạn怎么办?

Token Preny có thời hạn (thường 7 ngày). Khi hết hạn:

1. Đăng nhập lại https://app.preny.ai
2. Lấy token mới theo hướng dẫn trên
3. Cập nhật lại environment:
```bash
export PRENY_TOKEN="new-token-here"
```

## Bảo mật Token

⚠️ **Lưu ý quan trọng:**

- KHÔNG chia sẻ token với người khác
- KHÔNG commit token vào git repository
- Token có quyền truy cập dữ liệu doanh nghiệp của bạn
- Nếu lộ token, đổi mật khẩu Preny ngay lập tức

## Troubleshooting

### Lỗi: "Invalid token"
- Token đã hết hạn → Lấy token mới
- Token không đúng format → Copy lại đầy đủ

### Lỗi: "Unauthorized"
- Token không hợp lệ → Đăng nhập lại Preny
- Workspace không tồn tại → Liên hệ admin

### Lỗi: "Rate limit exceeded"
- Đã vượt giới hạn request → Đợi 1 phút và thử lại
