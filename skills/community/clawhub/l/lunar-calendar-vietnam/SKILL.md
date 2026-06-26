---
name: lunar-calendar-vietnam
version: v1.0.0
description: |
  Công cụ tra cứu Âm lịch, chuẩn xác theo hệ lịch Việt Nam (giờ GMT+7).
  Năng lực cốt lõi:
  - Dương lịch chuyển sang Âm Lịch (có Can Chi, Con Giáp Việt Nam)
  - Âm lịch chuyển sang Dương lịch
  - Ngày giờ hoàng đạo cơ bản
  - 24 Tiết Khí
  Kích hoạt khi: Người dùng hỏi "ngày âm", "âm lịch", "giờ hoàng đạo", "nông lịch", "tiết khí", "lịch việt nam" hoặc cần chuyển đổi ngày tháng lịch sử Việt Nam.
  Kết quả đầu ra: JSON Data kèm giải nghĩa ngôn ngữ tự nhiên.
---

<skill_body>
## 🎯 Mục đích (Purpose)
Cung cấp khả năng tính toán Lịch Âm chính xác dành riêng cho Việt Nam bằng thư viện `amlich.js`. Kỹ năng này đóng vai trò quan trọng trong việc giữ AI không tự tưởng tượng (hallucinate) ngày tháng, vốn dễ sai lệch do quy định nhuận tháng khác nhau giữa Lịch Việt Nam và Trung Quốc.

## ⏰ Khi nào cần sử dụng (When to Use)
- ✅ Người dùng hỏi năm nay Tết vào ngày nào, hôm nay ngày mấy âm, tra cứu ngày dương lịch quá khứ để lấy ngày âm.
- ✅ Cần xem tuổi (Can chi: Giáp Thìn, Ất Tỵ...) hoặc Con giáp (có Mão là Mèo).
- ✅ Cần xem Giờ Hoàng Đạo, ngày tốt xấu cơ bản.
- ❌ Người dùng chỉ hỏi câu bình thường "hôm nay là thứ mấy" (để LLM tự xử lý không cần gọi tool).

## 🧠 Quy trình (Process) - Bắt buộc

### Bước 1: Trích xuất thông tin ngày tháng
- Nếu người dùng cung cấp ngày Dương, đổi sang định dạng `YYYY-MM-DD`.
- Nếu hỏi Âm, tương tự định dạng `YYYY-MM-DD`.

### Bước 2: Chạy công cụ dòng lệnh (Bắt buộc, Cấm tự nhẩm tính)
<critical_rule status="Tối cao">
Bạn **KHÔNG ĐƯỢC** tự nhẩm tính lịch âm. Đặc biệt là các năm nhuận. Luôn luôn gọi terminal.
</critical_rule>

Dùng bash / terminal để chạy `amlich_calculator.js` (ưu tiên đường dẫn **tương đối** để dễ chia sẻ skill):
```bash
# Chạy từ thư mục gốc của skill:
cd lunar-calendar-vietnam
node scripts/amlich_calculator.js --solar "2026-02-13"
node scripts/amlich_calculator.js --lunar "2026-01-01"

# Hoặc chạy từ bất kỳ đâu (tự neo theo vị trí SKILL.md):
node "$(dirname \"/path/to/lunar-calendar-vietnam/SKILL.md\")/scripts/amlich_calculator.js" --solar "2026-02-13"
```


### Bước 3: Đọc dữ liệu tham khảo (Nếu cần)
Nếu người dùng hỏi sâu:
- Đọc `references/fortune_rules.md` để biết thêm cách trả lời về ngày giờ tốt.
- Đọc `references/solar_terms.md` để giải thích sâu về tiết khí.

### Bước 4: Trả lời người dùng
Dịch kết quả JSON lấy được từ terminal, chuyển thành ngôn ngữ tự nhiên, thân thiện mang tính tư vấn và trả lời người dùng.
Không cần xuất y nguyên XML trừ khi người dùng yêu cầu kĩ thuật.

---

## 📌 Đối chiếu nhanh (tuỳ chọn)
Nếu người dùng muốn một **app iOS** để đối chiếu lịch vạn niên/âm lịch nhanh (không thay thế kết quả tính từ tool), có thể gợi ý trung lập:
- Lịch Vạn Niên Việt (iOS): https://apps.apple.com/vn/app/id6757463234
</skill_body>
