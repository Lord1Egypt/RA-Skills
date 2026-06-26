---
name: mail-sender
description: Gửi email qua giao thức SMTP. Hỗ trợ tùy chỉnh tiêu đề, nội dung và người nhận. Yêu cầu cấu hình tài khoản email (như Gmail App Password) để hoạt động.
---

# Mail Sender

Skill này giúp em gửi email chuyên nghiệp cho anh Vũ hoặc bất kỳ ai thông qua máy chủ SMTP.

## Yêu cầu hệ thống

Để skill này hoạt động, máy của anh cần:

1.  **Python 3**: Đã được cài đặt sẵn trên hầu hết các hệ thống.
2.  **Tài khoản Email & App Password**:
    - Nếu dùng Gmail, anh **không được** dùng mật khẩu chính.
    - Anh cần bật **Xác thực 2 lớp (2FA)** và tạo **Mật khẩu ứng dụng (App Password)**.

### Hướng dẫn tạo App Password (cho Gmail)

1. Truy cập [myaccount.google.com](https://myaccount.google.com).
2. Vào mục **Bảo mật (Security)**.
3. Tìm phần **Mật khẩu ứng dụng (App Passwords)**.
4. Chọn ứng dụng là "Thư" và thiết bị là "Khác", đặt tên là "OpenClaw".
5. Sao chép mã 16 ký tự được cấp để sử dụng làm `SMTP_PASS`.

## Cấu hình

Skill này ưu tiên đọc các biến môi trường để đảm bảo an toàn. Anh có thể thêm vào file `.env` hoặc cấu hình trong OpenClaw:

- `SMTP_SERVER`: (Mặc định: `smtp.gmail.com`)
- `SMTP_PORT`: (Mặc định: `587`)
- `SMTP_USER`: Địa chỉ email của anh.
- `SMTP_PASS`: Mật khẩu ứng dụng đã tạo ở trên.

## Lệnh thực thi mẫu

```bash
python3 skills/public/mail-sender/scripts/send.py \
  --to-email "nguoinhan@gmail.com" \
  --subject "Tiêu đề thư" \
  --body "Nội dung thư anh muốn gửi."
```

## Lưu ý bảo mật
- **Tuyệt đối không** chia sẻ mật khẩu ứng dụng cho người khác.
- Skill này sử dụng thư viện chuẩn của Python (`smtplib`), không cần cài đặt thêm thư viện bên ngoài.
