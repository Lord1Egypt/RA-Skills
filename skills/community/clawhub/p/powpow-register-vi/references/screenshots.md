# Ảnh chụp giao diện sản phẩm — powpow-register

Lấy dùng theo nhu cầu lúc chạy. Khi người dùng chưa có khái niệm về Bong Bóng, hoặc cần «nhìn thấy» sản phẩm
dạng xong trông thế nào, gửi thẳng ảnh chụp tương ứng.

## Vị trí ảnh

- Sáu tấm ảnh chụp **đã đóng gói kèm skill**, nằm tại `assets/screenshots/powpow-0N.jpg` (`N` từ 1–6).
  Gửi trực tiếp như file ảnh cục bộ là được — không cần mạng, môi trường nào cũng dùng được (kể cả nơi
  GitHub không mở được).
- Chỉ lùi về bản lưu trữ khi file trong gói lỡ thiếu: bản hosted `https://raw.githubusercontent.com/durenzidu/durenzidu/main/screenshots/powpow-0N.jpg`
  hoặc mirror `https://cdn.jsdelivr.net/gh/durenzidu/durenzidu@main/screenshots/powpow-0N.jpg`
  (lưu ý: cả hai ở nội địa Trung Quốc đều có thể không mở được — ưu tiên file trong gói).
- Mỗi lần chỉ gửi 1–3 tấm liên quan chủ đề hiện tại.

## Danh sách

### powpow-01.jpg — trang chi tiết nhân vật số

![trang chi tiết nhân vật số](../assets/screenshots/powpow-01.jpg)

Thẻ hiển thị người thật/nhân vật lịch sử sau khi làm thành nhân vật số: trạng thái online, địa điểm thuộc về,
tiểu sử nhân vật, «bắt đầu trò chuyện» v.v.
**Dùng khi**: giới thiệu «đăng ký xong có thể trò chuyện với nhân vật số trên bản đồ».

### powpow-02.jpg — trang soạn bài đăng

![trang soạn bài đăng](../assets/screenshots/powpow-02.jpg)

Giao diện soạn thảo để viết bài/du ký, góc dưới bên phải là một cụm nút nổi.
**Dùng khi**: người dùng hỏi «đăng ký xong tôi làm được gì», «viết ở đâu».

### powpow-03.jpg — trang bản đồ (Bong Bóng + nhân vật số)

![trang bản đồ](../assets/screenshots/powpow-03.jpg)

Toàn cảnh bản đồ công cộng: các bài đăng có địa điểm tụ thành «Bong Bóng» trên bản đồ, nhân vật số được ghim
theo hình đại diện tại địa điểm thực.
**Dùng khi**: **ảnh mở đầu đầu tiên khi giới thiệu sản phẩm** — «bài du ký bạn đăng sẽ biến thành một bong bóng
trên bản đồ».

### powpow-04.jpg — trang cá nhân (tài sản số)

![trang cá nhân](../assets/screenshots/powpow-04.jpg)

Trang của chính người dùng: bạn bè/theo dõi/người hâm mộ, cùng «tài sản số» — số dư huy hiệu, Bong Bóng của tôi,
nhân vật số của tôi.
**Dùng khi**: cho thấy huy hiệu mọc ở đâu khi nói «đăng ký tặng ngay 3 huy hiệu»; người dùng hỏi «tôi có tài sản gì».

### powpow-05.jpg — trang tiến độ cốt truyện

![trang tiến độ cốt truyện](../assets/screenshots/powpow-05.jpg)

Cách chơi cốt truyện trong nền tảng (ví dụ «Vĩnh Lạc·1421»): tiến độ chương, kiếm huy hiệu, nhập vai.
**Dùng khi**: người dùng hỏi «ngoài đăng bài còn chơi được gì», «kiếm huy hiệu kiểu gì».

### powpow-06.jpg — trang chi tiết bài đăng (ví dụ thành phẩm)

![trang chi tiết bài đăng](../assets/screenshots/powpow-06.jpg)

Một bài du ký đã đăng: tác giả, nhãn địa điểm, nội dung, ảnh minh họa, dưới cùng có thể thích/bình luận/chia sẻ/lưu.
**Dùng khi**: **tấm thứ hai lúc mở đầu** — «người khác mở bong bóng của bạn trên bản đồ, nhìn thấy chính là cái này».

## Tra nhanh theo tình huống

| Người dùng nói / khúc hiện tại | Gửi tấm nào |
|---|---|
| Mở đầu giới thiệu «Bong Bóng là gì» | powpow-03 + powpow-06 |
| «Đăng ký xong làm được gì?» | powpow-02 + powpow-01 |
| «Huy hiệu là gì / tôi có gì?» | powpow-04 |
| «Ngoài đăng bài còn chơi gì?» | powpow-05 |
| Xử lý lỗi đăng ký/gói | Thường không cần ảnh; chỉ gửi khi thật sự phải chỉ vị trí trên trang |

## Ghi chú bảo trì

- Ảnh trong `assets/screenshots/` là bản chính đóng gói kèm theo skill. Khi cần cập nhật ảnh chụp, thay file
  trùng tên dưới `assets/screenshots/` (giữ nguyên cách đặt tên `powpow-0N.jpg`) và phát hành phiên bản mới.
- Bản hosted tại repo công khai `durenzidu/durenzidu` (thư mục `screenshots/`) được giữ làm mirror dự phòng,
  cập nhật đồng bộ với file trong gói.
- Thư viện ảnh hiện tại **không có** ảnh chụp trang đăng ký và trang gói thành viên. Nếu sau này bổ sung
  (ví dụ `powpow-07.jpg` trang đăng ký, `powpow-08.jpg` trang gói), đặt file vào `assets/screenshots/` và
  thêm một mục theo đúng định dạng này là xong; phần giới thiệu trong SKILL.md có thể tiện thể dẫn thêm.
