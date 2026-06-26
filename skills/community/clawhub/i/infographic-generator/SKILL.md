---
name: infographic-generator
description: Tạo ảnh infographic, banner hoặc poster trực tiếp bằng 1 prompt gửi tới API tạo ảnh qua 9Router.
---
## 📋 0. QUY TRÌNH XÁC NHẬN THÔNG TIN BẮT BUỘC (MANDATORY)

Khi người dùng yêu cầu tạo ảnh, **bắt buộc** phải có đầy đủ các thông tin rõ ràng dưới đây. Nếu người dùng đưa ra yêu cầu chung chung hoặc thiếu bất kỳ yếu tố nào, bạn **phải hỏi lại để làm rõ** trước khi tiến hành tạo ảnh:

*   **Tiêu đề / Chủ đề chính**: Tiêu đề tiếng Việt cần viết lên ảnh (Ví dụ: *“10 điều nên làm vào mỗi buổi sáng”*).
*   **Nội dung chi tiết các mục**: Các ý nội dung để đưa vào các ô/phần của ảnh. (Lưu ý: Bạn có thể tự tìm kiếm thông tin qua web-search hoặc tự diễn giải chi tiết dựa trên chủ đề nếu người dùng đồng ý, nhưng cần xác nhận rõ).
*   **Phong cách thiết kế**: Chọn một trong các phong cách chính (Tin tức báo chí, Cẩm nang hoạt hình 2D, hay Layout Neo-Brutalism).
*   **Tỷ lệ khung hình / Layout**: (Ví dụ: Hình vuông 1:1, Poster dọc 2:3, hay Banner ngang 16:9).
*   **Dòng Footer**: Dòng chữ bản quyền ở cạnh dưới (Ví dụ: *“designed by Williams - trợ lý của tuanminhhole”*).

> [!IMPORTANT]
> **Tuyệt đối không tự tiện tạo ảnh khi chưa rõ các yếu tố trên.** Hãy phản hồi lịch sự, liệt kê các yếu tố còn thiếu và đưa ra các tùy chọn/ví dụ gợi ý để người dùng chọn nhanh.

---

Khi người dùng yêu cầu tạo ảnh infographic, tin tức, cẩm nang, hoặc poster bằng tiếng Việt, hãy sử dụng skill này để gọi trực tiếp API tạo ảnh qua script `image-generator.js`. Phương pháp này tạo ra các tác phẩm thiết kế đồng nhất và tuyệt đẹp chỉ bằng một câu prompt chi tiết duy nhất.

## 🚀 1. LỆNH THỰC THI

Để tạo ảnh, hãy gọi tool `exec` để chạy lệnh:
`node skills/infographic-generator/image-generator.js "<prompt chi tiết bằng tiếng Anh>" <tên_ảnh>.png`

_(Ví dụ: `node skills/infographic-generator/image-generator.js "A professional grid infographic..." output.png`)_

---

## 📐 2. QUY ĐỊNH KÍCH THƯỚC & TỶ LỆ (ASPECT RATIO)

Khi gọi API, mặc định kích thước là tỷ lệ **1:1** (hình vuông). Tuy nhiên, hãy tùy biến linh hoạt theo yêu cầu của người dùng bằng cách điều chỉnh từ khóa mô tả tỷ lệ và khung hình trong prompt:

- **Mặc định (1:1)**: Thêm từ khóa `square aspect ratio, 1:1 square canvas` vào prompt. Phù hợp cho các infographic dạng ô lưới hoặc bài đăng mạng xã hội thông thường.
- **Poster dọc (Vertical Poster)**: Thêm từ khóa `vertical poster aspect ratio, 2:3 portrait format, vertical infographic` vào prompt. Phù hợp cho cẩm nang chi tiết có nhiều mục (3-9 mục).
- **Landscape (16:9)**: Thêm từ khóa `16:9 landscape aspect ratio, wide horizontal banner` vào prompt. Phù hợp cho banner nằm ngang, ảnh bìa.

---

## ✍️ 3. QUY ĐỊNH FOOTER BẮT BUỘC

Mọi ảnh infographic/poster được tạo ra bằng skill này bắt buộc phải có dòng chữ bản quyền nằm ở cạnh dưới, canh giữa:

- **Nội dung chữ bắt buộc**: `"designed by Williams - trợ lý của tuanminhhole"` (hoặc tên bot tương ứng đang chạy).
- **Cách mô tả trong prompt**: Thêm vào cuối prompt mô tả chi tiết:
  _"At the bottom center of the image, there is a clean and tiny centered footer text that reads: 'designed by Williams - trợ lý của tuanminhhole'"_

---

## 🎨 4. BA PHONG CÁCH THIẾT KẾ CHỦ ĐẠO

Hãy chọn 1 trong 3 phong cách dưới đây tùy thuộc vào ngữ cảnh yêu cầu:

### Phong cách 1: Tin tức báo chí / News Editorial

- **Đặc điểm**: Bố cục chuyên nghiệp, chia nhiều cột dọc/ngang (multi-column), sử dụng các đường kẻ mỏng hoặc nét đứt mảnh để phân chia các ô tin tức rõ ràng.
- **Phông chữ**: Font tiêu đề Serif (có chân) sang trọng, font nội dung Sans-serif (không chân) hiện đại.
- **Minh họa**: Icon dạng vector phẳng (flat vector icons), tối giản, chuyên nghiệp.
- **Từ khóa prompt gợi ý**: `news editorial infographic style, newspaper grid layout, clear divider lines, minimal serif headers, flat vector icons, professional business theme, clean corporate colors.`

### Phong cách 2: Cẩm nang/Hướng dẫn chi tiết

- **Đặc điểm**: Bố cục lưới (ví dụ: 3x3 grid) gồm nhiều ô được đánh số thứ tự (1, 2, 3...). Mỗi ô có nền màu pastel nhẹ nhàng (như xanh lá nhạt, kem nhạt, vàng nhạt) với viền bo góc tròn mềm mại. Có hình mascot (như chú heo đất đeo kính, két sắt, nhân vật hoạt hình) xuất hiện làm điểm nhấn.
- **Phông chữ**: Font chữ tròn, thân thiện, rõ ràng.
- **Minh họa**: Icon hoạt hình 2D sống động, nhiều màu sắc.
- **Từ khóa prompt gợi ý**: `detailed guide infographic poster, 3x3 numbered grid layout, rounded pastel cards, cute 2D cartoon mascot, playful vector icons, warm cream background, clear numbered badges.`

### Phong cách 3: Layout Neo-Brutalism hoạt hình

- **Đặc điểm**: Đường viền đen dày nổi bật (thick dark borders), đổ bóng cứng màu đen (hard solid drop shadows), màu sắc tương phản mạnh mẽ (Neo-Brutalism), phong cách hoạt hình 2D phẳng, hiện đại và trẻ trung.
- **Phông chữ**: Font chữ in đậm, cá tính và không chân.
- **Minh họa**: Mascot và các icon phẳng nét vẽ dày cá tính.
- **Từ khóa prompt gợi ý**: `neo-brutalism infographic poster, vector cartoon flat 2D style, thick dark solid borders, hard black drop shadows, bright vibrant background cards (yellow, cyan, lime green, orange), playful modern bold typography.`

---

## 🔤 5. QUY TẮC PHÒNG TRÁNH LỖI FONT TIẾNG VIỆT

Mô hình tạo ảnh hỗ trợ ghi text tiếng Việt cực tốt, nhưng để tránh việc AI tự động dùng các font chữ lạ bị lỗi hiển thị dấu tiếng Việt, hãy áp dụng nghiêm ngặt các quy tắc sau:

1. **Chỉ định phông chữ tiêu chuẩn**: Trong prompt, ghi rõ tên các font chữ phổ biến hỗ trợ Unicode tiếng Việt tốt như: **Arial, Inter, Montserrat, Roboto, Plus Jakarta Sans, Fredoka** (chỉ dùng cho phong cách hoạt hình).
   _Ví dụ: "in clean bold Arial font", "using modern Montserrat typeface"._
2. **Tránh phông chữ lạ**: Tuyệt đối **KHÔNG** sử dụng các từ khóa như `decorative, script, handwritten, gothic, calligraphy, futuristic fonts` vì chúng hầu như không hỗ trợ tiếng Việt và sẽ tạo ra chữ lỗi phông rất xấu.
3. **Định dạng Text rõ ràng**: Đặt toàn bộ các đoạn text tiếng Việt cần hiển thị trong dấu nháy đơn hoặc nháy kép để mô hình nhận diện chính xác phần văn bản cần viết.
   _Ví dụ: At the top, the main title in bold Arial font reads: 'BÍ KÍP TRÁNH NÓNG MÙA HÈ'._

---

## 📝 6. MẪU PROMPT CHUNG CHO BOT LLM (TÙY CHỈNH THEO YÊU CẦU)

### Công thức Prompt Tiếng Anh (Khuyên Dùng cho API)

```text
An infographic poster with [Tỷ lệ khung hình] and [Loại nền].
Art style is modern illustration style mixed with hand-drawn elements.
At the top, the main title in clean bold [Tên Font tiếng Việt chuẩn] reads: '[TIÊU ĐỀ TIẾNG VIỆT LỚN]'.
The layout is divided into [Số lượng] cards or sections [Bố cục chia ô từ trên xuống dưới / Bố cục ô lưới / Quy trình cách thức].
The background and accent colors of the cards are [Màu sắc hài hòa tương ứng phù hợp với chủ đề].
Each card contains a clean flat vector illustration representing [Mô tả ngắn gọn hình vẽ minh họa] and a clear text label in bold [Tên Font tiếng Việt chuẩn] reads: '[NHÃN TIẾNG VIỆT CHO TỪNG Ô]'.
The text throughout the image must be clean, legible, and easy to read.
At the bottom center of the image, there is a clean and tiny centered footer text that reads: 'designed by Williams - trợ lý của tuanminhhole'.
High-resolution, high quality, professional infographic poster, no spelling mistakes.
```
