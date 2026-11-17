# Quy trình đăng ký chi tiết — powpow-register

Để tra cứu khi xử lý lỗi. Mọi quy tắc đều đến từ mã nguồn nền tảng (kiểm tra nhất quán frontend-backend
Next.js), có ghi xuất xứ. Khi nền tảng cập nhật thì lấy hành vi thực tế trên mạng làm chuẩn.

## Lối vào

- Trang đăng ký: https://global.powpow.online/register
- Trang đăng nhập: https://global.powpow.online/login
- Trang gói thành viên: https://global.powpow.online/subscription
- Nếu vào từ link chia sẻ có kèm `?next=...`, sau khi đăng ký + thanh toán xong sẽ tự động nhảy về trang gốc.

## Trường biểu mẫu và quy tắc

| Trường | Bắt buộc | Quy tắc | Xuất xứ mã |
|---|---|---|---|
| Ảnh đại diện | Không bắt buộc | Ảnh ≤5MB, không hỗ trợ SVG; máy chủ tự nén (khi >100KB nén về 400×400 / chất lượng 90) | `src/app/api/auth/register/route.ts` |
| Tên người dùng | Bắt buộc | 2~50 ký tự, sau khi trim chuyển sang **chữ thường** để lưu (Tom và tom coi là cùng một tên người dùng, cả đầu đăng ký lẫn đầu đăng nhập đều không phân biệt hoa thường) | Như trên (zod schema) |
| Mật khẩu | Bắt buộc | 8~100 ký tự, phải đồng thời chứa chữ hoa, chữ thường, chữ số | Như trên |
| Xác nhận mật khẩu | Bắt buộc | Trùng với mật khẩu (chỉ kiểm tra phía frontend) | `src/app/(public)/register/page.tsx` |
| Biệt danh | Không bắt buộc | ≤100 ký tự; không điền thì mặc định lấy tên người dùng | register route |
| Email | **Bắt buộc** | Định dạng email hợp lệ, ≤255 ký tự; một email chỉ đăng ký được một tài khoản | register route |
| Mã xác minh email | **Bắt buộc** | 6 chữ số; **hiệu lực 10 phút**; xác minh thành công là vô hiệu luôn; gửi lại sẽ đánh dấu mã cũ là đã dùng | `src/lib/email-verification.ts` |
| Số điện thoại | Không bắt buộc | Số nội địa Trung Quốc bắt đầu `1[3-9]` tổng 11 chữ số; một số điện thoại chỉ liên kết được một tài khoản | register route |

Trang còn cung cấp ba nút đăng nhập bên thứ ba: **Google, Watcha, tài khoản Huawei**
(`GoogleSignInButton` / `WatchaLoginButton` / `HuaweiLoginButton`). Tài khoản bên thứ ba không có mật khẩu cục bộ,
sau này đăng nhập bằng mật khẩu sẽ nhận được «tài khoản này chưa đặt mật khẩu, vui lòng dùng cách khác để đăng nhập».

## Tham số giới hạn tần suất và chống dò máy

| Hành vi | Giới hạn | Xuất xứ |
|---|---|---|
| Nộp đăng ký | **3 lần/phút/IP**, vượt là 429 | `src/lib/rate-limit.ts` `REGISTER_RATE_LIMIT` |
| Gửi mã xác minh | Cùng IP 1 lần/phút **và** cùng email 1 lần/phút, vượt là 429; nút phía frontend đếm ngược 60 giây | `src/app/api/auth/register/send-code/route.ts` |
| Kiểm tra mã xác minh | Mỗi email trong 10 phút tối đa thử **5 lần**, chạm trần thì dù mã đúng cũng từ chối, phải gửi mã lại | `src/lib/email-verification.ts` |
| Gửi mã quên mật khẩu | 1 lần/phút/IP | `src/app/api/auth/forgot-password/route.ts` |
| Đăng nhập | 5 lần/phút/IP; cùng một tài khoản thất bại liên tiếp **5 lần thì khóa 30 phút** (423), trong lúc đó đếm ngược số lần còn lại | `src/app/api/auth/login/route.ts`, `rate-limit.ts` |

**Hành vi bảo vệ quyền riêng tư**: khi gửi mã xác minh / quên mật khẩu, nếu email đã được đăng ký hoặc không tồn
tại, giao diện đều trả về cùng một thông báo thành công, không tiết lộ email đã đăng ký hay chưa.

## Sự tương đương giữa chế độ agent thao tác hộ và đăng ký qua trang web

Script của skill gọi là **cùng một loạt API công khai** (`/api/auth/register`, `send-code`, `login`,
`/api/auth/me`), đi qua đường kiểm tra, giới hạn tần suất và lỗi hoàn toàn giống nộp biểu mẫu trang đăng ký —
mọi quy tắc trong file này đối với hai chế độ như nhau. Trình tự script và hợp đồng lệnh xem
`references/agent-flow.md`.

## Luồng Trạng Thái Sau Khi Đăng Ký Thành Công

> **Giai đoạn dùng thử miễn phí (bắt đầu từ 2026-10-18; hành vi thực tế của nền tảng là chuẩn)**: tài khoản mới đăng ký có thể **dùng mọi tính năng trực tiếp**
> (bảng tin, bản đồ, nhân vật số, điểm danh, v.v.) không cần trả tiền; tài khoản chưa đăng ký gói không còn bị chặn khỏi các trang nội dung. Việc "chặn pending"
> mô tả trong mục này là trạng thái thông thường sau khi giai đoạn dùng thử kết thúc — khi đến lúc đó, hành vi thực tế trên mạng là chuẩn.

1. Người dùng được lưu với `accountStatus: 'pending'` và **3 huy hiệu khởi tạo** (route register).
2. Máy chủ cũng gắn hai cookie HttpOnly: JWT (vào trang trực tiếp được) và pendingUserToken (chứng thực danh tính cho luồng đăng ký gói).
3. Ở trạng thái thông thường (giai đoạn dùng thử kết thúc / không có giai đoạn miễn phí), trang đăng ký phát hiện `pending_payment` → chuyển hướng sang `/subscription`
   (giữ tham số trả về `next`); ở chế độ agent đại diện, `me?token=…&redirect=/subscription` cho hiệu ứng tương đương.
   **Trong giai đoạn dùng thử miễn phí, bước này không kích hoạt** — sau khi đăng ký, vào thẳng trang chủ và bắt đầu dùng.
4. Thanh toán xong → `accountStatus` thành `active` (**Alipay tự kích hoạt phía máy chủ qua notify**;
   PayPal kích hoạt qua Webhook; mã QR WeChat xác nhận thủ công; Huawei IAP đi qua `activate-huawei`).
   Chi tiết ở `payment-and-activation.md`.

Ở trạng thái thông thường, tài khoản chưa kích hoạt (pending) gọi các API lõi (bảng tin, bản đồ, chat nhân vật số, điểm danh, v.v.) sẽ bị 403;
link bài đăng chia sẻ là ngoại lệ (vẫn mở công khai). Trong giai đoạn dùng thử miễn phí, việc chặn này tạm ngưng và mọi thứ đều mở.
## Bảng xử lý lỗi thường gặp

| Hiện tượng | Nguyên nhân | Xử lý |
|---|---|---|
| 「用户名已存在」 (tên người dùng đã tồn tại) | Tên người dùng bị chiếm (không phân biệt hoa thường) | Đổi một tên người dùng khác |
| 「邮箱已被使用」 (email đã được dùng) | Email đã đăng ký rồi | Đổi email; hoặc chuyển sang đăng nhập + «quên mật khẩu» để tìm lại tài khoản cũ |
| 「邮箱验证码错误或已过期」 (mã xác minh sai hoặc hết hạn) | Mã nhập sai / quá 10 phút / thử sai quá 5 lần bị từ chối | Bấm «gửi lại», dùng mã trong **bức thư mới nhất** |
| Không nhận được mã xác minh | Giới hạn 60 giây; hoặc rơi vào hộp thư rác/thư quảng cáo | Đợi hết đếm ngược rồi gửi lại; lục thư mục thư rác |
| 「手机号已被使用」 (số điện thoại đã được dùng) | Số điện thoại đã liên kết tài khoản khác | Bỏ số điện thoại (trường tùy chọn) hoặc đổi số |
| 「注册请求过于频繁」 (yêu cầu đăng ký quá dày) / 429 | Đăng ký 3 lần/phút/IP chạm trần | Chờ vài phút rồi thử lại |
| 409 「用户名或邮箱已被注册」 (tên người dùng hoặc email đã được đăng ký) | Đúng khoảnh khắc nộp bị đụng tên với người khác (lưới an toàn cạnh tranh) | Đổi tên người dùng hoặc email rồi thử lại |
| 「图片大小不能超过5MB」 (kích thước ảnh không quá 5MB) / 「不支持 SVG」 (không hỗ trợ SVG) | Ảnh đại diện không đạt chuẩn | Đổi ảnh hoặc bỏ qua ảnh đại diện |
| Người dùng bấm link đăng nhập nhưng rơi vào trang gói hội viên (thay vì trang chủ) | Giai đoạn dùng thử miễn phí đã kết thúc, tường phí của nền tảng đã trở lại | Theo luồng thanh toán đăng ký gói ở bước 7 trong SKILL.md; sau khi đăng ký gói, chạy `refresh-login` rồi gửi link trang chủ |
| Đăng ký thành công nhưng đăng nhập trả về 403 "请完成订阅以激活账户" | Tài khoản vẫn pending, và nền tảng không trong giai đoạn dùng thử miễn phí (trạng thái mong đợi trước khi trả tiền) | Trong giai đoạn dùng thử miễn phí sẽ không xảy ra; nếu xảy ra nghĩa là giai đoạn dùng thử đã kết thúc — hoàn tất đăng ký gói trước; nếu trả tiền rồi vẫn 403 thì đã dùng JWT cũ — ở chế độ script chạy `refresh-login` trước để đổi lấy trạng thái đăng nhập mới |
| Đăng nhập 423 「账户已锁定」 (tài khoản đã bị khóa) | Mật khẩu sai liên tiếp 5 lần | Chờ 30 phút |
| Đăng nhập 401 「还剩 N 次尝试机会」 (còn N lần thử) | Mật khẩu sai, gần chạm mức khóa | Nghĩ cho kỹ rồi thử, hoặc đi thẳng «quên mật khẩu» |
| 「该账号未设置密码，请使用其他方式登录」 (tài khoản này chưa đặt mật khẩu, vui lòng dùng cách khác để đăng nhập) | Tài khoản bên thứ ba (Google/Watcha/Huawei) | Dùng nút bên thứ ba ban đầu để đăng nhập |
| 「该账号已注销」 (tài khoản này đã hủy) | Tài khoản đã deactivate | Cần đăng ký lại |

## Mẹo vặt về đăng nhập (để tiện xử lý lỗi luôn)

Đăng nhập hỗ trợ nhập ba trong một **tên người dùng / email / số điện thoại** (bất kỳ cái nào cũng được coi
là tên tài khoản).
Quên mật khẩu: trang đăng nhập → «Quên mật khẩu» → nhập email đăng ký nhận mã 6 chữ số → đặt lại.
