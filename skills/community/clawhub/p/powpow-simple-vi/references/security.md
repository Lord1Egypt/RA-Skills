# Kiến trúc bảo mật & API nền tảng

> Chỉ dùng cho bảo trì/xử lý sự cố. Khi chạy theo SKILL.md không cần đọc tệp này.

## Vì sao kỹ năng này phân phát an toàn

Kỹ năng này **không chứa khóa bí mật nào của nền tảng**:

| Mục | Đảm bảo |
|---|---|
| Khóa bí mật nền tảng | Không có trong gói — mọi thao tác đi qua API HTTP của chính nền tảng |
| Danh tính | JWT từ một lần đăng nhập thật; bạn chỉ có thể đăng với tư cách chính mình |
| Mật khẩu người dùng | Không bao giờ lưu; chỉ dùng đúng một lần trong bộ nhớ để lấy token ngắn hạn (~7 ngày) |
| Giới hạn tần suất / kiểm duyệt | Server ép buộc (10 bài/giờ/người dùng, kiểm duyệt nội dung) |
| Khó Unsplash | Do người dùng cung cấp, tùy chọn (ảnh là tùy chọn) |

Kỹ năng không bao giờ đọc, ghi hay phát tệp chứa chứng từ. Trạng thái duy nhất nó ghi là token
phiên của chính người dùng, nằm trong thư mục trạng thái của người dùng (xem dưới), tuyệt đối
không nằm trong gói kỹ năng.

`config.json` chỉ chứa `{ "platformUrl", "unsplashAccessKey"(tùy chọn),
"sessionMaxAgeDays", "skillVersion" }`. Tuyệt đối không thêm khóa Supabase, service role
hay admin token vào kỹ năng này.

### Tệp tuyệt đối không được rời khỏi máy của người dùng
- `<POWPOW_STATE_DIR>/session.json` (mặc định `~/.powpow/session.json`) — JWT của người dùng
  đang đăng nhập (tự hết hạn sau ~7 ngày). Được ghi vào thư mục trạng thái của người dùng,
  tuyệt đối không ghi vào gói kỹ năng (có thể chỉ đọc).

## Các endpoint API nền tảng được sử dụng

- `POST /api/auth/login` — `{step:1, username, password}` → JWT (Cookie `powpow_token`)
- `GET  /api/digital-humans?scope=all&search=...` — liệt kê/tìm Người số (cần đăng nhập)
- `GET  /api/amap/place/text?keywords=...` — tìm tên nơi (cần đăng nhập; trả GCJ-02,
  geocode.js chuyển sang WGS-84 phía máy khách). Đường dẫn endpoint này là nội bộ của
  nền tảng, không được nêu với người dùng; trong thảo luận nội bộ gọi trung lập là dịch vụ
  tìm địa điểm (không bao giờ nói tên nhà cung cấp cho người dùng).
- `POST /api/upload/post-image` — tải ảnh cục bộ lên (multipart `file`; cần đăng nhập)
- `POST /api/posts` — tạo bài đăng (cần đăng nhập; server ép buộc giới hạn & kiểm duyệt)
- `GET  /api/posts/{id}` — xác minh một bài đăng
- `DELETE /api/posts/{id}` — xóa bài của chính mình (dọn bài kiểm thử)
- `POST /api/digital-humans` — tạo Người số (cần đăng nhập; tiêu 2 huy hiệu, hết hạn 30 ngày)
- `POST /api/digital-humans/generate-avatar` — avatar AI từ thiết lập nhân vật
  (cần đăng nhập; 8–30 giây; theo thiết kế nền tảng cần URL ảnh tham chiếu)
- `GET  /api/badges/balance?userId=...` — kiểm tra trước số dư huy hiệu

Ghi chú: JWT được buộc với dấu vân thiết bị (User-Agent + Accept-Language). API client ghim
các header này lúc đăng nhập và tự dùng lại. Gặp `DEVICE_MISMATCH` hoặc 401: chỉ cần đăng nhập lại.
