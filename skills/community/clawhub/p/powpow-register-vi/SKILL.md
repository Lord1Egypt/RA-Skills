---
name: powpow-register
description: Giúp người dùng hoàn tất đăng ký PowPow (Bubble) và đăng nhập một cú click ngay trong cuộc hội thoại. Agent điền form thay người dùng (kể cả tải ảnh đại diện) và gửi mã xác minh email; người dùng chỉ cần cung cấp thông tin cơ bản và kiểm tra mã xác minh một lần — không rời cuộc hội thoại. Nền tảng hiện đang trong giai đoạn dùng thử miễn phí: tài khoản đã đăng ký có thể dùng ngay mọi tính năng; thanh toán gói hội viên (Alipay/PayPal) là nâng cấp tùy chọn, khi cần agent cũng lo việc tạo đơn và theo dõi tiền về. Kích hoạt khi người dùng nói "đăng ký Bubble", "tạo tài khoản powpow", "đăng ký Bubble thế nào", "giúp tôi tạo tài khoản powpow", "sign up powpow"; cũng xử lý các vấn đề đăng ký (không nhận được mã xác minh, tên người dùng/email đã dùng) và kích hoạt (đăng nhập báo "tài khoản chưa kích hoạt" / pending_payment, làm sao đăng ký gói/thanh toán, Bubble miễn phí hay trả phí). Yêu cầu Node ≥ 18; nếu không có sẽ tự động chuyển sang chế độ hướng dẫn thuần túy. Không lo việc đăng bài/tạo nhân vật số (đó là nhiệm vụ của powpow-simple), cũng như phát triển mã.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (trợ lý đăng ký Bong Bóng)

Dẫn dắt người dùng mới từ "chưa biết Bubble là gì" đến "đăng nhập một cú click, chơi được ngay" — toàn bộ trong cuộc hội thoại. Người dùng chỉ rời cuộc hội thoại đúng một lần: **để kiểm tra mã xác minh trong hộp thư**. Nền tảng hiện đang trong giai đoạn dùng thử miễn phí: sau khi đăng ký, mọi tính năng đều dùng được, không cần trả tiền; thanh toán gói hội viên là nâng cấp tùy chọn (agent cũng lo mở quầy thu ngân và theo dõi tiền về).

**Phiên bản 2.2.0** · 2026-10-18 (từ v2 trở đi là chế độ agent đại diện: hợp đồng script và toàn bộ trình tự ở `references/agent-flow.md`; quy tắc trường, giới hạn tần suất và xử lý lỗi ở `references/registration-flow.md`; kênh thanh toán ở `references/payment-and-activation.md`; danh sách ảnh chụp sản phẩm ở `references/screenshots.md`. Từ v2.1.0 agent cũng lo được gói PayPal, song song với Alipay. Từ v2.2.0 nền tảng bước vào giai đoạn dùng thử miễn phí: đăng ký xong đăng nhập một cú click là dùng được ngay; thanh toán trở thành nâng cấp tùy chọn — nếu người dùng mở link lại rơi vào trang gói hội viên, nghĩa là giai đoạn dùng thử đã kết thúc, hãy theo luồng thanh toán ở bước 7; luồng tự thích ứng, không cần sửa script)

## Môi trường chạy

- Script chính `scripts/powpow-register.mjs`: **không phụ thuộc**, cần **Node ≥ 18**. Trước khi bắt đầu, chạy một lần `node scripts/powpow-register.mjs status` để xác nhận môi trường hoạt động.
- Mọi request của script chỉ gửi về domain chính thức `https://global.powpow.online`.
- **Không có Node / script lỗi**: tự động chuyển sang chế độ hướng dẫn thuần túy — đưa cho người dùng trang đăng ký https://global.powpow.online/register và đồng hành hướng dẫn theo `references/registration-flow.md` (trong giai đoạn dùng thử miễn phí, đăng ký trên web cũng dùng được ngay như nhau). Đừng cố gắng chạy script mãi.
- Khôi phục sau khi hội thoại bị ngắt: chạy `status` trước để xem quy trình đang ở bước nào rồi tiếp tục.

## Trigger Conditions

- Ý định đăng ký: «đăng ký Bong Bóng», «tạo tài khoản powpow», «Bong Bóng đăng ký thế nào», «sign up powpow»
- Đăng ký bị kẹt: «không nhận được mã xác minh», «báo tên người dùng đã tồn tại», «mật khẩu cứ không đạt yêu cầu»
- Vấn đề sau đăng ký: "đăng nhập báo tài khoản chưa kích hoạt", "403 pending_payment", "trả tiền/đăng ký gói Bubble thế nào", "Bubble miễn phí hay trả phí"

**Không kích hoạt cho**: đăng bài/tạo nhân vật số (→ powpow-simple); phát triển code phía Web (xem các skill phát triển). Người dùng vừa muốn đăng ký vừa muốn đăng bài: chạy xong skill này trước, sau khi kích hoạt rồi giao cho powpow-simple.

## Tổng quan quy trình

| Bước | agent làm gì | Người dùng làm gì |
|---|---|---|
| 1 Giới thiệu sản phẩm | Giới thiệu + gửi ảnh chụp | Nhìn qua một chút |
| 2 Xác nhận thông tin | Chủ động gợi ý tên người dùng/biệt danh, mật khẩu chọn 1 trong 2, hỏi email | Xác nhận, cung cấp |
| 3 Gửi mã | `send-code` | —— |
| 4 Đọc lại mã | —— | Vào email xem mã 6 chữ số, gửi lại |
| 5 Gửi đăng ký | `register` (kèm tải thẳng ảnh đại diện), tự xử lý lỗi | —— |
| 6 Đăng nhập một cú click | `login-link(home)` vào thẳng trang chủ; nếu rơi vào trang gói hội viên thì sang bước 7 | Bấm link và bắt đầu dùng |
| 7 Nâng cấp gói hội viên (tùy chọn) | Chỉ khi người dùng muốn làm hội viên / giai đoạn miễn phí đã kết thúc: lo trọn luồng thanh toán | Chọn phương thức, trả tiền |
| 8 Kết thúc | `cleanup` + giao thông tin tài khoản + hướng dẫn trải nghiệm + gợi ý plugin | Bắt đầu chơi |

## Bước 1: giới thiệu sản phẩm + ảnh chụp (không được bỏ qua)

Đa số người dùng chưa từng thấy Bong Bóng. Việc đầu tiên không phải kể quy trình, mà là để họ **thấy** sản phẩm:

1. Giới thiệu Bong Bóng trong ~120 ký tự: biến những bức ảnh chụp tức thì thành một bài du ký, ghim lên bản đồ công cộng thành một «bong bóng»; bong bóng sẽ hạ nhiệt theo thời gian, lượt «thích» của người khác có thể hồi sinh nó; trên bản đồ còn có «nhân vật số» có thể trò chuyện. Địa chỉ nền tảng: https://global.powpow.online ; muốn xem video trước: https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Gửi ảnh chụp**. Ảnh chụp đã đóng gói kèm skill tại `assets/screenshots/powpow-0N.jpg` — gửi trực tiếp như file ảnh cục bộ, không cần mạng. Danh sách, nội dung từng ảnh và thời điểm sử dụng nằm trong `references/screenshots.md`. Bộ đôi hay dùng nhất lúc mở đầu: trang bản đồ (powpow-03) + trang chi tiết bài đăng (powpow-06).

Quy tắc ảnh chụp (quy tắc cứng):

- Ảnh chụp **đã đóng gói kèm skill** trong `assets/screenshots/` (`powpow-0N.jpg`) — gửi trực tiếp như file ảnh cục bộ; dùng được trong mọi môi trường, kể cả nơi GitHub không mở được.
- Mỗi lần chỉ gửi 1–3 ảnh liên quan chủ đề hiện tại, đừng nhét tất cả một lượt.
- Nếu file trong gói lỡ thiếu, lùi về các link lưu trữ được liệt kê trong `references/screenshots.md` (lưu ý: trong nội địa Trung Quốc có thể không mở được).

Giới thiệu xong, trao quyền lựa chọn cho người dùng: **«Nếu bạn muốn đăng ký, ba phút nữa ta tạo xong tài khoản ngay trong hội thoại; bạn chỉ cần xem mã xác minh trong email một lần.»**

## Bước 2: xác nhận thông tin đăng ký (mỗi lượt một câu hỏi, đừng hỏi hết một lượt)

- **Tên người dùng** (bắt buộc): **chủ động gợi ý một cái** từ bối cảnh hội thoại/tên người dùng hệ thống (2~50 ký tự, không phân biệt hoa thường); người dùng gật đầu thì dùng, muốn đổi thì đổi.
- **Mật khẩu** (bắt buộc; trước tiên cho chọn 1 trong 2):
  - Người dùng tự cung cấp → sau đó truyền cho script qua biến môi trường, **tuyệt đối không đưa vào tham số dòng lệnh**;
  - agent tạo → chạy `node scripts/powpow-register.mjs gen-password` và **gửi ngay mật khẩu vừa tạo cho người dùng lưu lại** (chỉ hiển thị một lần, sau đó không xuất hiện nữa).
- **Email** (bắt buộc): người dùng phải tự cung cấp — đây là mỏ neo định danh của tài khoản, **đừng đoán hộ**.
- **Biệt danh** (không bắt buộc): gợi ý mặc định giống tên người dùng.
- **Ảnh đại diện** (không bắt buộc): người dùng đưa đường dẫn ảnh cục bộ (≤5MB, không phải SVG) thì script tải thẳng; không có thì bỏ qua (nền tảng dùng logo mặc định); nếu bạn có khả năng tạo ảnh, có thể chủ động đề nghị làm giúp một tấm.
- **Số điện thoại** (không bắt buộc, số nội địa Trung Quốc): mặc định bỏ qua; chỉ hỏi khi người dùng chủ động muốn liên kết.

Xác nhận xong có thể chạy `prepare-suggest --username U --nickname N --email E` để ghi vào file trạng thái (sau đó register không cần truyền lại).

## Bước 3–4: mã xác minh qua email (đoạn duy nhất buộc phải rời hội thoại)

```
node scripts/powpow-register.mjs send-code --email <email>
```

Sau đó nói rõ với người dùng: **vào email tìm mã xác minh 6 chữ số, có hiệu lực 10 phút; nhớ xem cả thư mục spam/thư quảng cáo**; khi tìm thấy thì quay lại gửi mã cho bạn. Việc gửi có thời gian chờ 60 giây, đừng bấm liên tục.

## Bước 5: gửi đăng ký (agent thao tác hộ)

```
POWPOW_REGISTER_PASSWORD=<mật khẩu> node scripts/powpow-register.mjs register --code <mã> [--username U] [--nickname N] [--avatar <đường dẫn ảnh cục bộ>] [--phone P]
```

Thành công là tài khoản được tạo (trạng thái pending, kèm 3 huy hiệu khởi đầu). Các lỗi thường gặp được xử lý tự động, không làm gián đoạn người dùng:

| Lỗi | Xử lý |
|---|---|
| 「用户名已存在」 (tên người dùng đã tồn tại) | Tự động gợi ý biến thể (tên người dùng + số), khi người dùng xác nhận thì thử lại ngay (mã vẫn còn hiệu lực, không cần gửi lại) |
| 「邮箱已被使用」 (email đã được dùng) | Hỏi người dùng: đổi email, hay thật ra đã có tài khoản? (chuyển sang đăng nhập/quên mật khẩu) |
| 「邮箱验证码错误或已过期」 (mã xác minh sai hoặc hết hạn) | Quá 10 phút → chạy lại `send-code` |
| Gửi/đăng ký quá dày (429) | Chờ 1 phút rồi thử lại; chỉ cần báo người dùng một tiếng |

## Bước 6: Đăng Nhập Một Cú Click (sau đăng ký vào thẳng trang chủ)

1. Ngay sau khi đăng ký thành công:
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Gửi link cho người dùng: **bấm vào là vào thẳng trang chủ, đã đăng nhập sẵn**. Nền tảng hiện đang trong giai đoạn dùng thử miễn phí — sau khi đăng ký, mọi tính năng (bảng tin, bản đồ, nhân vật số, điểm danh, v.v.) đều dùng được, **không cần trả tiền**.
3. Nhờ người dùng xác nhận đã vào được; có hai trường hợp:
   - **Vào được trang chủ** → nhảy thẳng sang bước 8 để khép lại; quy trình đăng ký hoàn tất;
   - **Rơi vào trang gói hội viên** → giai đoạn dùng thử miễn phí của nền tảng đã kết thúc; nói với người dùng "giai đoạn dùng thử miễn phí đã hết, giờ cần đăng ký gói hội viên", sau đó theo bước 7 hoàn tất đăng ký gói, xong quay lại bước 8.
4. Nếu người dùng tự nguyện muốn nâng cấp hoặc ủng hộ nền tảng → cũng sang bước 7 (đăng ký gói là tự nguyện; đừng mời mọc).
## Bước 7: Nâng Cấp Gói Hội Viên (tùy chọn — chỉ khi bước 6 yêu cầu)

1. Trước tiên gửi link đăng nhập nửa vời để trang trả về sau thanh toán hiển thị đúng "Thanh toán thành công":
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Gửi link cho người dùng: bấm vào là trình duyệt mở thẳng trang gói hội viên, đã đăng nhập sẵn.
2. **Nhờ người dùng chọn phương thức thanh toán** — hiển thị cả hai kênh:
   - **Alipay (Trung Quốc đại lục / người dùng có Alipay)**: mua một lần theo thời hạn tương ứng, **không tự động gia hạn**
     - Tháng **¥6.99** (khuyên dùng để thử) / Quý **¥19.99** / Năm **¥69.99**
   - **PayPal (hải ngoại / người dùng không có Alipay)**: tự động gia hạn hàng tháng, hủy bất cứ lúc nào
     - Premium Monthly, khoảng **$1/tháng** (theo hiển thị trên trang gói hội viên; tự động gia hạn)
3. Khi người dùng đã chọn:
   - **Alipay**:
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal**:
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   Script trả về đường dẫn file trang thanh toán; **mở trực tiếp bằng lệnh hệ thống** (Windows: `start <file>`; macOS: `open <file>`; Linux: `xdg-open <file>`). Trình duyệt tự động nhảy sang quầy thu ngân chính thức Alipay/PayPal, nơi người dùng hoàn tất thanh toán hoặc uỷ quyền trừ tiền.
4. Chạy `query` mỗi 10–15 giây cho đến khi trả về `paid` hoặc `ACTIVE` (tiền về/uỷ quyền thường trong vài giây đến một phút). Nếu người dùng đóng trang thanh toán giữa chừng → chỉ cần `create-order` lại (đơn cũ / gói đang chờ tự đóng hoặc hết hạn sau 2 giờ; bỏ qua).
5. Kênh mã QR WeChat xác nhận thủ công, tiền về có thể chậm; Huawei IAP chỉ dùng được trong ứng dụng HarmonyOS. Skill không lo hai kênh này — sau khi trả tiền, người dùng quay lại báo agent, agent chạy `whoami` xác nhận tiền về trước, rồi gửi link trang chủ theo điểm 6 bên dưới.
6. Sau khi xác nhận tiền về, đổi lấy trạng thái đăng nhập mới nhất kèm quyền lợi gói hội viên, rồi gửi link vào thẳng trang chủ:
   ```
   POWPOW_REGISTER_PASSWORD=<mật khẩu> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Gửi link cho người dùng: **bấm vào là vào thẳng trang chủ với trạng thái hội viên đầy đủ**.
## Bước 8: Khép Lại

1. `node scripts/powpow-register.mjs cleanup` để dọn các file trạng thái tạm trên máy (thông tin đăng nhập phiên).
2. Đưa cho người dùng một "thẻ tài khoản": tên người dùng, email (mật khẩu không hiển thị lại — ở chế độ sinh mật khẩu, người dùng đã được nhờ lưu lại lúc sinh; nếu người dùng tự đặt thì họ tự biết).
3. Nhắc nhở về hội viên (nói một lần, đừng mời mọc): hiện đang trong giai đoạn dùng thử miễn phí, dùng được ngay; khi giai đoạn dùng thử kết thúc, tài khoản chưa đăng ký gói khi vào các trang nội dung sẽ bị chuyển hướng về trang gói hội viên — để dùng lâu dài, quay lại tìm agent đăng ký bất cứ lúc nào.
4. Hướng dẫn bước đầu: xem bản đồ, đăng nhật ký du lịch đầu tiên (→ chuyển giao cho powpow-simple).
5. Giới thiệu tiện ích mở rộng: skill `@durenzidu/powpow-integration` và plugin `@durenzidu/openclaw-channel-powpow` — kết nối Bubble vào agent của chính người dùng; đưa lệnh cài nếu muốn.
6. Kết thúc bằng khối "bước tiếp theo".
## Conversation UX

Giữ đúng tông phục vụ quen thuộc của powpow:

- **Người dùng là chủ ngữ của câu**; «bạn có thể…» tốt hơn «tôi cần bạn…»; không giảng đạo, không đứng trên nhìn xuống.
- **Mỗi lượt chỉ tiến một quyết định**; trước khi xin thông tin, nêu lý do trước.
- **Cuối mỗi câu trả lời** là một khối «bước tiếp theo» cố định (dấu phân cách + 👉 + một hành động duy nhất + một câu «khi bạn làm xong, tôi sẽ…»), ví dụ:
  ```
  ────────────────────
  👉 Đến lượt bạn: vào email tìm mã 6 chữ số và gửi thẳng cho tôi
     (ngay khi nhận được, tôi tạo tài khoản cho bạn)
  ```
- **Không chủ động giảng bài bảo mật về mật khẩu**; không giải thích cơ chế bên trong, giới hạn tần suất hay thiết kế an toàn, trừ khi người dùng hỏi.
- Khi agent thao tác hộ càng phải báo tiến độ: sau mỗi bước script, nói một câu cho người dùng biết vừa xảy ra chuyện gì («tài khoản đã tạo xong», «trang thanh toán đã mở cho bạn rồi»).

## Quy tắc cứng

- **An toàn thông tin đăng nhập**: mật khẩu chỉ truyền cho script qua biến môi trường `POWPOW_REGISTER_PASSWORD`, **tuyệt đối không** đưa vào tham số dòng lệnh (nhìn thấy trong danh sách tiến trình), không ghi vào bất kỳ file nào (chế độ tạo mật khẩu hiển thị một lần để người dùng lưu, sau đó không nhắc lại). Mã xác minh chỉ dùng cho giao diện đăng ký chính thức và vứt bỏ sau khi dùng.
- **Ranh giới chính thức**: mọi request chỉ gửi về `https://global.powpow.online` (đã tích hợp sẵn trong script); tuyệt đối không gửi thông tin người dùng tới địa chỉ bên thứ ba nào.
- **Ranh giới thanh toán**: agent chỉ tạo đơn, mở trang thu ngân, tra tiền về; **tuyệt đối không** đụng vào tài khoản Alipay/PayPal/chứng từ thanh toán của người dùng, cũng tuyệt đối không hứa «trả tiền hộ».
- **Tường phí không phải lỗi**: trong giai đoạn dùng thử miễn phí hiện tại, mọi trang nội dung đều mở; nếu người dùng bấm link trang chủ lại rơi vào trang gói hội viên, nghĩa là giai đoạn dùng thử đã kết thúc — hướng dẫn đăng ký gói qua bước 7. Đừng tìm cách vượt tường phí, và đừng giải thích cơ chế nội bộ cho người dùng.
- **Tự do lùi lại**: nếu ở bất kỳ bước nào người dùng muốn tự làm, hoặc môi trường không chạy được script, cứ lùi về chế độ hướng dẫn thuần bất cứ lúc nào — đưa link, giảng quy tắc, cùng xử lý lỗi.
- Đừng bịa quy tắc của nền tảng: quy tắc trường, nội dung lỗi, tham số giới hạn đều đến từ code nền tảng (`references/registration-flow.md` có ghi nguồn); nền tảng cập nhật thì lấy hành vi thực tế làm chuẩn.
- Khi trình bày ảnh chỉ dùng ảnh chụp trong gói `assets/screenshots/` (công dụng từng ảnh xem trong `references/screenshots.md`).
- Mỗi lượt kết thúc bằng khối «bước tiếp theo», để người dùng luôn biết mình cần làm gì lúc này.
