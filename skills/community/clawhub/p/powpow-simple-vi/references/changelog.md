# Changelog — powpow-simple-vi

Lịch sử phiên bản (không cần khi chạy; chỉ dùng cho bảo trì/xử lý sự cố).

## 1.0.2 — 2026-09-25

Làm mới siêu dữ liệu danh mục cửa hàng (chỉ siêu dữ liệu — không thay đổi chức năng).

- Tên hiển thị, chủ đề và danh mục (communication/lifestyle/creative) được nâng lên chuẩn của dòng powpow-register.
- Ghi chú: 1.0.1 chỉ là cập nhật phiên bản nội bộ phía cửa hàng, không có mục riêng trong tệp này.

## 1.0.0 — 2026-09-20

Phát hành lần đầu bản tiếng Việt. Fork từ `powpow-simple` v5.7.3, tương đương chức năng;
`scripts/` giống hệt từng byte (đã xác minh SHA256). Chỉ thay văn bản và siêu dữ liệu —
không đổi bất kỳ dòng script nào.

- **Đặt tên hiển thị theo chức năng**: 「PowPow Simple VI - Đăng bài và ghim Người số lên
  bản đồ công khai」 (tương ứng tên hiển thị mô tả của bản tiếng Trung; slug định tuyến
  vẫn là `powpow-simple-vi`).

- **SKILL.md dịch trọn sang tiếng Việt**: câu kích hoạt (tiếng Việt, tiếng Anh và tiếng
  Trung), UX hội thoại (bảng giọng điệu, mẫu mở đầu, khối 「Bước tiếp theo」), toàn bộ
  workflow 8 bước, tạo Người số, xử lý lỗi và mọi quy tắc cứng.
- **Thêm quy tắc ngôn ngữ (quy tắc cứng)**: Cuộc trò chuyện luôn theo ngôn ngữ của người
  dùng — bản tiếng Việt phục vụ người dùng ở mọi ngôn ngữ.
- **Văn bản hóa placeholder đúng như script nhận diện**: `{{dh}}` / `{{数字人}}`,
  `{{loc}}` / `{{位置}}`, `{{img}}` / `{{图}}` (bả danh tiếng Trung là token nguyên văn
  mà compose.js nhận — tuyệt đối không bịa token mới).
- **Thêm ghi chú trung thực về bản địa hóa**: tìm kiếm địa điểm và thư viện Người số của
  nền tảng hiện tập trung ở tiếng Trung; banner trang xem trước và giao diện sản phẩm
  trong ảnh chụp màn hình là tiếng Trung.
- **Dịch README.md**, gồm cả lưu ý cho người duyệt (ngữ cảnh dành cho người duyệt, vốn
  được thêm ở bản tiếng Trung 5.7.3).
- **Dịch references/**: security.md, file-structure.md, screenshots.md.

## Lịch sử kế thừa (từ powpow-simple, bản tiếng Trung)

Gói này kế thừa toàn bộ hành vi của `powpow-simple` tới v5.7.3. Các cột mốc chính của
bản tiếng Trung:

- **5.7.3 — 2026-09-19**: Giảm nhiễu khi kiểm toán (danh sách năng lực trong description,
  viết lại security.md, lưu ý cho người duyệt, văn bản hóa đường dẫn phiên). Không đổi script.
- **5.7.2 — 2026-09-19**: Bỏ nhận định sai 「like làm bong bóng hồi sinh」; thêm ảnh chụp
  màn hình sản phẩm (6 ảnh + mirror jsdelivr). Không đổi script.
- **5.7.1 — 2026-09-18**: Đổi tên biến môi trường thành `POWPOW_PASSWORD`
  (sửa lỗi chính tả 「PowWow」 tồn tại lâu).
- **5.7.0 — 2026-09-18**, **5.6.0 / 5.5.0 — 2026-09-18**, **5.4.1 / 5.4 — 2026-09-17**,
  **5.3 — 2026-09-17**: tiến hóa trước đó của pipeline nhiều script (đăng nhập/xử lý phiên,
  semantics hỏng cứng của placeholder compose, hạ cấp mã hóa địa lý, tạo Người số, lọc sức
  khỏe). Chi tiết đầy đủ xem `references/changelog.md` của bản tiếng Trung.
