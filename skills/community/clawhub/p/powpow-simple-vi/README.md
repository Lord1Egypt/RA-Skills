# PowPow Simple VI — Đăng bài và ghim Người số lên bản đồ công khai

Trợ lý PowPow, bản tiếng Việt (OpenClaw): biến ảnh hay tư liệu của bạn thành một bút ký du lịch
rồi đăng lên PowPow, hoặc làm một người/nhân vật thành Người số (digital human) biết trò chuyện,
ghim lên bản đồ công khai.

Đây là bản tiếng Việt của [powpow-simple](https://clawhub.ai/durenzidu/skills/powpow-simple)
(tương đương chức năng v5.7.3; các script giống hệt từng byte).

## Cài đặt

```
openclaw skills install @durenzidu/powpow-simple-vi
```

## Yêu cầu môi trường

- Node.js 18+ (script dùng `fetch` toàn cục, không phụ thuộc bên thứ ba)
- Tài khoản PowPow: https://global.powpow.online/register

## Thư mục trạng thái

Gói kỹ năng giữ nguyên chỉ đọc. Token đăng nhập và cấu hình người dùng nằm trong thư mục trạng thái:

- Mặc định: `~/.powpow/`
- Có thể ghi đè bằng biến môi trường `POWPOW_STATE_DIR`

Muốn tùy biến địa chỉ nền tảng hoặc Unsplash key, chỉ cần đặt `config.json` vào thư mục trạng thái
— giá trị của nó sẽ đè lên mặc định trong gói.

## Ví dụ sử dụng

```
cd <thư-mục-kỹ-năng>
node scripts/doctor.js                                   # tự kiểm + thăm dò phiên
node scripts/login.js <username>                         # đăng nhập (mật khẩu qua stdin, không lưu đĩa)
node scripts/geocode.js "地坛公园" --limit 5              # tên nơi -> tọa độ
node scripts/match-digital-human.js "读书 作家" --limit 3  # ghép Người số
node scripts/compose.js --text-file post.txt --loc "地坛公园" --lng 116.408195 --lat 39.952372 --image @/duong/dan/tuyet/doi/cover.jpg --out post-draft.html
node scripts/publish.js post-draft.html                  # đăng bài
node scripts/verify.js <post-id>                         # xác minh sau khi đăng
node scripts/delete-post.js <post-id>                    # xóa (dọn bài kiểm thử)
```

Đường dẫn cục bộ cho `--image` **bắt buộc phải là đường dẫn tuyệt đối**.

Ghi chú: tìm kiếm địa điểm và thư viện Người số của nền tảng hiện tập trung ở tiếng Trung;
người dùng ngoài vùng tiếng Trung có thể dán tên và chủ đề bằng ngôn ngữ của mình.

## Bảo mật

- Không chứa bất kỳ khóa nào của nền tảng; mọi thao tác đều qua API công khai của nền tảng + JWT của chính người dùng.
- Mật khẩu chỉ dùng đúng một lần khi đăng nhập, không lưu đĩa; token hết hạn sau khoảng 7 ngày.
- Chi tiết xem `references/security.md`.

## Lưu ý cho người duyệt (SkillSpector / manual review)

- Đây là **kỹ năng kiểu chỉ thị**: SKILL.md điều phối một pipeline nhiều script. Mỗi script
  dưới `scripts/` là một bước được văn bản hóa của quy trình đăng bài (đăng nhập → tự kiểm →
  mã hóa địa lý → ghép → dựng → đăng → xác minh), không phải công cụ ẩn độc lập.
- `delete-post.js` chỉ xóa bài của chính người dùng đang đăng nhập
  (`DELETE /api/posts/{id}`, giới hạn bởi JWT, server ép buộc) và được văn bản hóa tại
  Bước 8 trong SKILL.md để dọn bài kiểm thử. Năng lực này cũng được khai báo trong
  description của kỹ năng.
- Không kèm bất kỳ khóa bí mật nào. `config.json` chỉ chứa giá trị mặc định. JWT phiên
  được ghi vào thư mục trạng thái của người dùng (`POWPOW_STATE_DIR`, mặc định
  `~/.powpow/session.json`), tuyệt đối không nằm trong gói kỹ năng. Mật khẩu không bao giờ
  được lưu.
- Mọi biến môi trường sử dụng (`POWPOW_STATE_DIR`, `POWPOW_PASSWORD`, `UNSPLASH_ACCESS_KEY`)
  đều tùy chọn và được khai báo trong frontmatter của SKILL.md (`metadata.openclaw.envVars`).
- Gói này là bản tiếng Việt của `powpow-simple`; script giống hệt từng byte với v5.7.3 của
  gói gốc (chỉ văn bản và siêu dữ liệu được dịch).

## Giấy phép

MIT-0 (giấy phép chung của ClawHub).

## Liên kết

- Trang chủ: https://global.powpow.online
- Bản đồ: https://global.powpow.online/map
- Bản tiếng Trung: https://clawhub.ai/durenzidu/skills/powpow-simple
- Bản tiếng Anh: https://clawhub.ai/durenzidu/skills/powpow-simple-en
- Bản tiếng Đức: https://clawhub.ai/durenzidu/skills/powpow-simple-de
- Bản tiếng Nhật: https://clawhub.ai/durenzidu/skills/powpow-simple-ja
