---
name: learning-memory
description: Tự tiến hóa bộ nhớ dài hạn MEMORY.md và đóng gói kỹ năng tự động.
---

## 🧠 Quy tắc Tự tiến hóa Bộ não & Trí nhớ dài hạn (Autonomous Mode)

Để Agent hoạt động thông minh, nhớ lâu và tự cải tiến kỹ năng một cách tự động, hãy áp dụng bộ quy tắc dưới đây vào lõi suy nghĩ của bạn:

### 1. Ghi nhớ dài hạn chủ động (Durable Memory Writing)

- **Chủ động cập nhật**: Khi nhận thấy một quy tắc mới, lỗi vừa debug thành công, thay đổi trong hành vi/yêu cầu của User hoặc cấu hình hệ thống → **bắt buộc** sử dụng công cụ sửa file để ghi nhận trực tiếp vào file [MEMORY.md](MEMORY.md) (hoặc file memory tương ứng của workspace).
- **Không thụ động**: Tuyệt đối không đợi hệ thống Dreaming ban đêm quét tự động. Hãy ghi chép ngay dưới dạng gạch đầu dòng ngắn gọn, cô đọng nhất.

### 2. Tự động đóng gói Kỹ năng (Autonomous Skill Synthesis)

- **Phát hiện quy trình lặp**: Khi thực hiện thành công một chuỗi thao tác phức tạp (cào dữ liệu, xử lý file excel, thiết lập API...), hãy tự động viết một script Javascript helper (ví dụ: lưu vào thư mục `skills/` trong workspace) để tự động hóa toàn bộ quy trình đó.
- **Tự cập nhật registry**: Cập nhật file [TOOLS.md](TOOLS.md) để ghi chép lại lệnh gọi của kỹ năng vừa tạo. Các phiên làm việc sau chỉ cần chạy lệnh đó thay vì viết lại logic từ đầu.

### 3. Phản tư cuối phiên làm việc (Self-Reflection Loop)

- Ở cuối mỗi phiên làm việc lớn, hãy tự chạy quy trình phản tư:
  1. _Có bài học kỹ thuật hay thói quen nào của User cần ghi nhớ không?_ $\rightarrow$ Cập nhật `MEMORY.md`.
  2. _Có quy trình nào lặp lại vừa làm nên được đóng gói không?_ $\rightarrow$ Tạo file Skill.
  3. _Có thông tin cũ nào trong bộ nhớ đã bị thay đổi/lỗi thời không?_ $\rightarrow$ Dọn dẹp và cập nhật `MEMORY.md`.

## 🛠️ LỆNH CÀI ĐẶT (INSTALL)

Để tự động cập nhật bộ quy tắc này vào tất cả các Agent đang chạy trong hệ thống, hãy chạy:
`node install.js`

Để khôi phục (restore) file gốc trước khi patch:
`node install.js --restore`
