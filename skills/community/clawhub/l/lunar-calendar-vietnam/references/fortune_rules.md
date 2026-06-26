# Quy Tắc Xem Ngày Tốt Xấu (Hoàng Lịch Việt Nam)

Tham khảo nhanh dành cho OpenClaw Agent trả lời người dùng về các vấn đề Âm lịch. Nếu người dùng hỏi "ngày này tốt hay xấu", "có hợp cưới hỏi không", v.v. hãy sử dụng thông tin từ file này để sinh câu trả lời tự nhiên. Tuyệt đối không copy paste toàn bộ file này cho người dùng.

## 1. Giờ Hoàng Đạo
Giờ Hoàng Đạo là giờ tốt trong ngày để tiến hành những việc quan trọng. Ngược lại là giờ Hắc Đạo (giờ xấu).
Lệnh `node scripts/amlich_calculator.js` sẽ trả về danh sách các can chi của Giờ Hoàng Đạo trong ngày.
Ví dụ: `Tý, Sửu, Thìn, Tỵ, Mùi, Tuất`.
(Lưu ý: Bạn cần dịch Can Chi sang khung giờ thực tế: Tý: 23h-1h, Sửu: 1h-3h, Dần: 3h-5h, Mão 5h-7h, Thìn 7h-9h, Tỵ 9h-11h, Ngọ 11h-13h, Mùi 13h-15h, Thân 15h-17h, Dậu 17h-19h, Tuất 19h-21h, Hợi 21h-23h).

## 2. Việc Nên và Không Nên Làm (Cơ bản)
Lưu ý: Lịch Âm Việt Nam phức tạp và tuỳ chỉnh theo vùng miền nên script hiện tại giả lập trả về `suitable` và `avoid`. Khi trả lời, hãy khuyên người dùng thông tin mang tính chất tham khảo văn hoá dân gian.
- **Cưới hỏi (Giá thú)**: Thích hợp ngày Hoàng Đạo, kị ngày Hắc Đạo, sát chủ, tam nương.
- **Xây nhà (Động thổ)**: Cần ngày hoàng đạo, tránh tháng Ngâu (Tháng 7 Âm) và các ngày kiêng kị.
- **Khai trương**: Chọn ngày hoàng đạo, giờ hoàng đạo ban sáng.

## 3. Khác biệt với Lịch Trung Quốc
- Con giáp: Lịch Việt Nam dùng **Mão (Mèo)** thay cho Thỏ. Lịch Việt dùng Trâu (Sửu) thay cho Bò.
- Múi giờ: Lịch Việt Nam tính theo múi giờ GMT+7, khác biệt với GMT+8 của Trung Quốc. Do đó có một số tháng nhuận hoặc ngày mùng 1 sẽ lệch 1 ngày so với lịch Trung Quốc. Điều này hoàn toàn bình thường. Mọi phép tính bằng `amlich.js` là chuẩn xác cho Việt Nam.
