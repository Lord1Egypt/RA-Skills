# powpow-register

Trợ lý đăng ký PowPow Bong Bóng (bản OpenClaw): đưa một người dùng mới từ «không biết Bong Bóng là gì» đến
«tài khoản kích hoạt, đăng nhập một chạm, bắt đầu chơi» — giới thiệu sản phẩm (kèm ảnh chụp giao diện),
agent thao tác hộ việc đăng ký (kèm tải ảnh đại diện), đặt đơn gói thành viên qua Alipay hoặc PayPal và theo dõi tiền về,
đăng nhập một chạm bằng link kép, xử lý lỗi.

**Từ v2.0.0 là chế độ agent đại diện, từ v2.2.0 còn thích ứng với giai đoạn dùng thử miễn phí của nền tảng**: script cốt lõi `scripts/powpow-register.mjs` không phụ thuộc thư viện
(Node ≥ 18); người dùng chỉ rời hội thoại đúng một lần: để kiểm tra mã xác minh trong hộp thư. Trong giai đoạn dùng thử miễn phí hiện tại, tài khoản đã đăng ký dùng được mọi tính năng ngay — thanh toán gói hội viên là tùy chọn; nếu giai đoạn dùng thử kết thúc và người dùng rơi vào trang gói hội viên, luồng tự chuyển sang đường thanh toán. Không có Node, hoặc khi người dùng muốn tự làm, tự động chuyển sang chế độ hướng dẫn thuần túy.

## Cài đặt

```
openclaw skills install @durenzidu/powpow-register
```

## Tính năng

1. **Giới thiệu sản phẩm**: mở đầu ~120 ký tự + ảnh chụp giao diện đóng gói kèm skill (`assets/screenshots/`
   có 6 tấm: trang bản đồ, trang chi tiết bài đăng v.v., chọn gửi 1–3 tấm theo tình huống; không cần dịch vụ
   lưu ảnh bên ngoài, dùng được khi ngoại tuyến).
2. **Đăng ký hộ**: agent chủ động gợi ý tên người dùng/biệt danh, mật khẩu chọn 1 trong 2 (người dùng cung cấp
   hoặc agent tạo), gửi và nộp mã xác minh, tải thẳng ảnh đại diện (≤5MB, không phải SVG), tự xử lý lỗi thường
   gặp (bị trùng/hết hạn/giới hạn tần suất).
3. **Đăng nhập một cú click (hai link)**: ngay sau khi đăng ký thành công, link đăng nhập đưa người dùng vào thẳng trang chủ (trong giai đoạn dùng thử miễn phí, một cú click là dùng được);
   nếu rơi vào trang gói hội viên (giai đoạn dùng thử kết thúc) hoặc người dùng muốn nâng cấp thì theo luồng đăng ký gói — sau khi tiền về, đổi lấy trạng thái đăng nhập mới và link hội viên đầy đủ đưa vào trang chủ
   (qua cầu nối chính thức `me?token=` của nền tảng, tự gắn cookie HttpOnly).
4. **Thanh toán gói**: cả Alipay (tháng ¥6.99 / quý ¥19.99 / năm ¥69.99,
   mua đứt một lần không tự động gia hạn) lẫn PayPal (Premium Monthly, khoảng $1/tháng, tự động gia hạn, hủy bất cứ lúc nào) đều do agent thao tác hộ đặt đơn + luân phiên tra tiền về;
   quét mã WeChat / Huawei IAP thì chỉ dẫn đường.
5. **Xử lý lỗi**: không nhận được mã xác minh, tên người dùng/email bị trùng, 403 chưa kích hoạt, tài khoản
   bị khóa    v.v. — các vấn đề thường gặp, tất cả đến từ mã nguồn nền tảng và có ghi rõ xuất xứ.

## Cấu trúc file

```
powpow-register/
├── SKILL.md                            # Chỉ dẫn chính (điều kiện kích hoạt, quy trình 8 bước, chuẩn tông giọng, quy tắc cứng)
├── README.md
├── .clawhubignore
├── assets/
│   └── screenshots/                    # Ảnh chụp sản phẩm đóng gói kèm (powpow-01~06.jpg)
├── scripts/
│   └── powpow-register.mjs             # Script chính (không phụ thuộc Node≥18, 11 lệnh con)
└── references/
    ├── agent-flow.md                   # Hợp đồng script, trình tự đầy đủ, cơ chế link kép, thiết kế an toàn
    ├── registration-flow.md            # Quy tắc trường, giới hạn tần suất, bảng xử lý lỗi (kèm nguồn mã)
    ├── payment-and-activation.md       # Hợp đồng Alipay vibepay, chuỗi kích hoạt, xử lý từng kênh
    └── screenshots.md                  # Danh sách ảnh chụp trong gói + tra nhanh theo tình huống
```

## An toàn

- **Mật khẩu** chỉ truyền vào tiến trình script qua biến môi trường, tuyệt đối không đưa vào tham số dòng lệnh,
  không ghi vào đĩa, không vào file trạng thái; mật khẩu do agent tạo chỉ hiển thị một lần để người dùng lưu.
- **Mã xác minh** chỉ dùng cho giao diện đăng ký chính thức, vứt bỏ sau khi dùng; file trạng thái
  (email/tên người dùng/token/số đơn) nằm trong thư mục tạm của hệ thống, kết thúc quy trình `cleanup`
  dọn sạch một phím.
- **Thanh toán**: agent chỉ tạo đơn, mở trang thu ngân, tra tiền về; tuyệt đối không đụng vào tài khoản Alipay / PayPal
  hay chứng từ thanh toán của người dùng, tuyệt đối không trả tiền hộ. Việc thanh toán luôn diễn ra giữa người
  dùng và trang thu ngân chính thức.
- Mọi request chỉ gửi domain chính thức `https://global.powpow.online`; không chứa bất kỳ khóa nào.

## Giấy phép

MIT-0 (giấy phép thống nhất ClawHub).

## Liên kết

- Trang chủ: https://global.powpow.online
- Đăng ký: https://global.powpow.online/register
- Tìm hiểu Bong Bóng (video): https://www.bilibili.com/video/BV1Wu826UEVz/
