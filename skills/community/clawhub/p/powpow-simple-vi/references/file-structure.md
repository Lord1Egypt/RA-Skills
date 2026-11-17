# Cấu trúc tệp

> Chỉ dùng cho bảo trì/xử lý sự cố. Khi chạy theo SKILL.md không cần đọc tệp này.

```
powpow-simple-vi/
├── SKILL.md                          # tệp chính (giữ gọn; chi tiết nằm trong references/)
├── config.json                       # platformUrl + Unsplash key tùy chọn của người dùng (KHÔNG khóa bí mật; chỉ đọc)
├── scripts/
│   ├── doctor.js                     # tự kiểm lần đầu (node/cấu hình/mạng/phiên)
│   ├── login.js                      # username/password → JWT (mật khẩu không lưu, nhập ẩn)
│   ├── compose.js                    # DỰNG HTML BÀI ĐĂNG BẰNG MỘT LỆNH (cách duy nhất được hỗ trợ; toàn cục bộ)
│   ├── publish.js                    # tải ảnh cục bộ + POST /api/posts với tư cách người dùng đang đăng nhập
│   ├── verify.js                     # xác minh bài đăng theo ID qua API nền tảng
│   ├── delete-post.js                # xóa bài của chính mình (dọn bài kiểm thử)
│   ├── geocode.js                    # tên nơi → ứng viên WGS-84 (người dùng xác nhận)
│   ├── list-digital-humans.js        # liệt kê/tìm với bộ lọc sức khỏe
│   ├── match-digital-human.js        # chủ đề → ứng viên khỏe mạnh đã xếp hạng
│   ├── create-digital-human.js       # tạo Người số cho bản đồ (2 huy hiệu, hết hạn 30 ngày; avatar: tạo/tải lên/URL)
│   ├── search-image.js               # Unsplash (key của người dùng, tùy chọn; cũng phân giải liên kết trang ảnh)
│   ├── upload-image.js               # ảnh cục bộ → kho nền tảng → URL công khai (publish.js dùng)
│   └── lib/
│       ├── api-client.js             # client API nền tảng (JWT, header ghim)
│       ├── dh-match.js               # bộ lọc sức khỏe DH chung + xếp hạng chủ đề (tên 3 lần, mô tả 1 lần, che thuật ngữ)
│       ├── coord-transform.js        # chuyển đổi GCJ-02 ↔ WGS-84 (nghịch đảo lặp)
│       └── html-formatter.js         # thành phần HTML + đếm chữ hỗ trợ CJK
└── references/
    ├── changelog.md                  # lịch sử phiên bản (gói này: 1.0.0; kế thừa: 5.3 → 5.7.3)
    ├── security.md                   # kiến trúc bảo mật + danh sách API nền tảng
    ├── screenshots.md                # danh sách ảnh chụp màn hình sản phẩm + liên kết ngoài
    └── file-structure.md             # tệp này
```

Ghi chú: phiên đăng nhập (`session.json`) **tuyệt đối không được ghi vào gói kỹ năng**; nó nằm
trong thư mục trạng thái của người dùng (`POWPOW_STATE_DIR`, mặc định `~/.powpow/`) và hết hạn
sau ~7 ngày (kỹ năng giữ biên 6 ngày cho việc đăng nhập lại).

Script trong gói này giống hệt từng byte với `powpow-simple` v5.7.3 — chỉ khác văn bản
và siêu dữ liệu.
