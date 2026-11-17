# Quy trình agent thao tác hộ và hợp đồng script — powpow-register

Chi tiết thực thi từng bước trong SKILL.md. Mọi lệnh đều là `node scripts/powpow-register.mjs <lệnh con> [tham số]`,
script **không phụ thuộc**, cần **Node ≥ 18**, mọi request chỉ gửi `https://global.powpow.online`.

## Thiết kế an toàn (vì sao thiết kế như vậy)

| Thiết kế | Lý do |
|---|---|
| Mật khẩu chỉ truyền qua biến môi trường `POWPOW_REGISTER_PASSWORD` | Tham số dòng lệnh của tiến trình nhìn thấy được với các tiến trình khác trên cùng máy (mặt rò rỉ argv), biến môi trường được script đọc rồi dùng ngay |
| Mật khẩu **tuyệt đối không ghi vào file trạng thái**, tuyệt đối không xuất hiện trong log | File trạng thái có thể lưu lại trên đĩa; chế độ tạo trong hội thoại chỉ hiển thị một lần là để người dùng lưu lại |
| File trạng thái nằm trong thư mục tạm của hệ thống (`os.tmpdir()/powpow-register-state.json`, 0600) | Chỉ chứa năm trường email / username / nickname / token / outTradeNo, `cleanup` dọn sạch một phím |
| JWT agent nhận được đổi sang cookie trình duyệt qua endpoint chính thức `me?token=` | Cầu chính thức nền tảng thiết kế cho WebView HarmonyOS; kiểm tra chữ ký chỉ tra chữ ký + thời hạn, không buộc vân tay thiết bị nên trình duyệt người dùng dùng được |
| Thanh toán chỉ làm create-order / query / mở trang thu ngân | Hành động trả tiền và chứng từ thanh toán mãi mãi ở giữa người dùng với trang thu ngân chính thức của Alipay, agent không đụng vào |

## Tham khảo lệnh

| Lệnh | Tham số chính | Công dụng / thời điểm |
|---|---|---|
| `status` | —— | Xem tiến độ quy trình (đọc file trạng thái); sau khi hội thoại bị ngắt chạy cái này trước |
| `gen-password` | —— | Sinh mật khẩu mạnh 24 ký tự (có cả hoa + thường + số), stdout hiển thị **chỉ một lần này** |
| `prepare-suggest` | `--username --nickname --email` | Ghi thông tin đã xác nhận vào file trạng thái (sau đó register không cần truyền lại) |
| `send-code` | `--email` | Kích hoạt nền tảng gửi mã xác minh 6 chữ số (hiệu lực 10 phút, thời gian chờ 60s) |
| `register` | `--code` (bắt buộc); `--username --nickname --avatar --phone` (không bắt buộc, file trạng thái có thì khỏi truyền) | Tạo tài khoản pending; mật khẩu đi qua biến môi trường `POWPOW_REGISTER_PASSWORD`; thành công thì JWT tự lưu vào file trạng thái |
| `login-link` | `--target pending` hoặc `--target home` | Tạo link đăng nhập một cú click (thiết kế hai link, xem bên dưới) |
| `create-order` | `--package monthly\|quarterly\|yearly` (mặc định là Alipay)<br>`--provider alipay\|paypal` | Tạo đơn thanh toán; Alipay trả về đường dẫn file trang thanh toán + outTradeNo; PayPal trả về đường dẫn file trang ủy quyền + subscriptionId (tự ghi vào file trạng thái) |
| `query` | —— | Tra trạng thái đơn/gói. Alipay: `paid / pending / closed / unknown`; PayPal: `ACTIVE / PENDING`; luân phiên 10–15s |
| `refresh-login` | Mật khẩu qua biến môi trường | Đăng nhập lại đổi **JWT mới** (tuyên bố gói từ NONE thành ACTIVE), sau khi tiền về bắt buộc phải chạy |
| `whoami` | —— | Dùng token trong file trạng thái tra tài khoản và trạng thái gói (kiểm tra kích hoạt đã ăn chưa) |
| `cleanup` | —— | Xóa file trạng thái (buộc chạy khi thu dọn) |

**Truyền biến môi trường** (mật khẩu mãi mãi không lên dòng lệnh):

```bash
# bash / zsh / WSL
POWPOW_REGISTER_PASSWORD='<mật khẩu>' node scripts/powpow-register.mjs register --code 123456
# PowerShell
$env:POWPOW_REGISTER_PASSWORD = '<mật khẩu>'; node scripts/powpow-register.mjs register --code 123456
# cmd
set POWPOW_REGISTER_PASSWORD=<mật khẩu> && node scripts/powpow-register.mjs register --code 123456
```

## Cơ Chế Hai Link (thiết kế cốt lõi)

Trạng thái đăng nhập của nền tảng là cookie HttpOnly, agent không thể tự gắn vào trình duyệt; cầu nối là endpoint chính thức
`/api/auth/me?token=<JWT>&redirect=<đường dẫn trong site>`: xác minh chữ ký → tự động tạo
phiên → `Set-Cookie: powpow_token` (HttpOnly / SameSite=Lax / 7 ngày) → kiểm tra
redirect (phải bắt đầu bằng dấu gạch chéo đơn, cấm `//` và dấu gạch chéo ngược, sau khi parse phải cùng origin) → 307 chuyển hướng tạm sang trang đích.

Có hai đích link, **ưu tiên sinh home trước, rồi quyết định có đi qua pending không dựa vào chỗ người dùng rơi vào**:

- **link home (mặc định, `--target home` → rơi vào `/`)**: sinh và gửi cho người dùng ngay sau khi đăng ký thành công.
  Trong giai đoạn dùng thử miễn phí, người dùng vào thẳng trang chủ, dùng được hết; **nếu bấm link lại rơi vào trang gói hội viên, nghĩa là giai đoạn dùng thử miễn phí đã kết thúc** — chuyển sang luồng thanh toán (xem bên dưới); không cần sửa script và không cần đăng ký lại.
- **link pending (dùng trong luồng thanh toán, `--target pending` → rơi vào `/subscription`)**:
  trình duyệt của người dùng vào trạng thái "đăng nhập nửa vời": trang gói hội viên và trang trả về sau thanh toán đều thấy và thao tác được. Sau khi tiền về,
  chạy `refresh-login` để đổi lấy JWT mới kèm quyền lợi ACTIVE, rồi gửi link home thêm lần nữa để có trạng thái hội viên đầy đủ.

## Trình Tự Đầy Đủ

### Luồng Nhanh (trong giai đoạn dùng thử miễn phí — đa số trường hợp)

```
1.  status                          # tự kiểm tra môi trường
2.  (bước 2: hội thoại xác nhận thông tin, mật khẩu tùy chọn; chế độ sinh: gen-password → nhờ người dùng lưu ngay)
3.  prepare-suggest --username U --nickname N --email E
4.  send-code --email E             # → người dùng kiểm tra mã trong hộp thư (lần duy nhất rời hội thoại)
5.  POWPOW_REGISTER_PASSWORD=*** register --code 123456 [--avatar pic.jpg]
6.  login-link --target home        # → gửi link cho người dùng; một cú click là vào trang chủ
7.  (người dùng xác nhận đã vào) → khép lại luôn: cleanup + thẻ tài khoản + hướng dẫn bước đầu
```

### Luồng Thanh Toán (khi người dùng muốn làm hội viên, hoặc giai đoạn miễn phí đã kết thúc)

```
1–5. Giống Luồng Nhanh (trạng thái đã có token sau khi register thành công)
6.  login-link --target pending     # → link đăng nhập nửa vời, trang trả về sau thanh toán vẫn hoạt động
7.  (người dùng chọn phương thức thanh toán)
    # Alipay: create-order --package monthly|quarterly|yearly
    # PayPal: create-order --provider paypal
8.  start <file trang thanh toán>   # Windows; macOS dùng open, Linux dùng xdg-open
    # → người dùng hoàn tất thanh toán/uỷ quyền tại quầy Alipay/PayPal (rời hội thoại)
9.  query (mỗi 10–15 giây) đến khi paid / ACTIVE
10. refresh-login                   # đổi lấy JWT mới kèm quyền lợi ACTIVE
11. login-link --target home        # → gửi link hội viên đầy đủ cho người dùng
12. whoami                          # xác nhận subscriptionStatus: ACTIVE (tùy chọn)
13. cleanup                         # dọn file trạng thái
```
## Ánh xạ lệnh → API nền tảng

| Lệnh script | Giao diện nền tảng |
|---|---|
| `send-code` | `POST /api/auth/register/send-code` |
| `register` | `POST /api/auth/register` (multipart, tải thẳng ảnh đại diện) |
| `login-link` | `GET /api/auth/me?token=…&redirect=…` (chính bản thân link, hiệu lực khi trình duyệt click) |
| `create-order` | `POST /api/payment/alipay/create-order` (Bearer, Alipay)<br>`GET /api/subscription/plans` + `POST /api/subscription/create` (Bearer, PayPal) |
| `query` | `GET /api/payment/alipay/query?outTradeNo=…` (Bearer, Alipay)<br>`GET /api/subscription/create` (Bearer, PayPal) |
| `refresh-login` | `POST /api/auth/login` (`{step:1, username, password}`) |
| `whoami` | `GET /api/auth/me?token=…` |

Xuất xứ quy tắc: trường đăng ký và giới hạn tần suất xem `registration-flow.md`; gói và chuỗi kích hoạt xem
`payment-and-activation.md` (đều ghi rõ file mã nguồn nền tảng).

## Xử lý lỗi cấp script

| Hiện tượng | Xử lý |
|---|---|
| `Phiên bản Node quá thấp` | Lùi về chế độ hướng dẫn thuần, đừng cố thử |
| Lỗi mạng / quá thời gian chờ | Thử lại một lần; vẫn thất bại thì nhờ người dùng kiểm tra mạng rồi tiếp tục (file trạng thái còn, chạy `status` từ đầu để khôi phục) |
| register báo lỗi nghiệp vụ (tên người dùng đã tồn tại v.v.) | Xử lý theo bảng ở bước 5 SKILL.md, **mã xác minh không cần gửi lại** (trong 10 phút vẫn còn hiệu lực) |
| register báo «mã xác minh sai hoặc hết hạn» | Quá thời hạn → `send-code` lại |
| Sau `create-order` người dùng đóng trang thanh toán | Chạy lại `create-order` thẳng (đơn cũ 2h tự đóng; gói PENDING của PayPal hết hạn sau 1h) |
| `create-order --provider paypal` báo 409 | Đã có một gói PayPal chưa hoàn tất; đợi 1h cho hết hạn, hoặc hoàn tất ủy quyền cũ trong trình duyệt |
| `query` mãi pending / PENDING | Người dùng có thể chưa trả; hỏi một câu. Thật sự đã trả → đi theo bảng xử lý trong payment-and-activation.md |
| Người dùng bấm link home nhưng rơi vào trang gói hội viên | Giai đoạn dùng thử miễn phí đã kết thúc → chuyển sang luồng thanh toán: `login-link --target pending` → chọn phương thức thanh toán → `create-order` |
| `refresh-login` 403 `pending_payment` | Giai đoạn dùng thử miễn phí đã kết thúc mà tiền chưa về; quay lại bước 9 tiếp tục poll, hoặc xác nhận người dùng đã hoàn tất thanh toán chưa |
| File trạng thái mất (tay lỡ xóa / đổi máy) | `whoami`/`refresh-login` không dùng được; nhờ người dùng mở trình duyệt đã từng mở link 1, trực tiếp tải lại trang gói để xác nhận trạng thái, hoặc đăng nhập lại (chế độ trang web) |

## Chế độ lùi (hướng dẫn thuần)

Gặp bất kỳ tình huống nào dưới đây thì lập tức lùi về hướng dẫn thuần kiểu v1, không thử script nữa:

- Không có Node ≥ 18 hoặc script liên tiếp hai lần thất bại cùng loại;
- Người dùng nói rõ «tôi tự thao tác trên trang web»;
- Chính sách công ty/thiết bị hạn chế script nối mạng.

Sau khi chuyển về: đưa trang đăng ký https://global.powpow.online/register (trong giai đoạn dùng thử miễn phí, đăng ký trên web cũng dùng được ngay như nhau; khi cần đăng ký gói, đưa thêm trang gói hội viên https://global.powpow.online/subscription ), xử lý sự cố song song theo quy tắc trong `registration-flow.md`, giữ cùng giọng điệu, và vẫn kết thúc mỗi lượt bằng khối "bước tiếp theo".
https://global.powpow.online/subscription , theo quy tắc trong `registration-flow.md` đồng hành xử lý lỗi,
tông giọng không đổi, mỗi lượt vẫn kết thúc bằng khối «bước tiếp theo».
