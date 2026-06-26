---
name: preny-analytics
description: Kết nối trực tiếp với Preny AI Chatbot để tự động tổng hợp và phân tích dữ liệu bán hàng theo thời gian thực.
metadata:
  openclaw:
    requires:
      bins: [curl, jq]
      env: [PRENY_TOKEN]
---

# Preny Analytics Skill

Kết nối trực tiếp với Preny AI Chatbot để tự động tổng hợp và phân tích dữ liệu bán hàng theo thời gian thực.

## Các chỉ số quan trọng

Cho phép theo dõi đầy đủ:

- Số lượng tin nhắn, hội thoại
- Hiệu quả chốt đơn, tỷ lệ chuyển đổi
- Phân tích theo tag khách hàng
- Trạng thái tương tác (đang chat, không phản hồi, đã lấy SĐT, …)
- Số điện thoại thu thập được
- Khách hàng mới / khách quay lại

## Điểm khác biệt

👉 Không cần đọc báo cáo thủ công

👉 Chỉ cần hỏi bằng ngôn ngữ tự nhiên, AI sẽ trả lời ngay

## Ví dụ câu hỏi

```
"Hôm qua có bao nhiêu khách mới?"
"Tỷ lệ chốt đơn tuần này thế nào?"
"Tag nào mang lại nhiều khách nhất?"
"Có bao nhiêu khách không phản hồi trong 3 ngày qua?"
"Thống kê tag màu"
"Phân loại khách hàng CRM"
```

## Phù hợp cho

- Chủ shop / sale cần xem nhanh hiệu quả
- Manager cần số liệu để ra quyết định
- Team CSKH muốn theo dõi chất lượng tương tác

## Cài đặt

Chỉ cần kết nối bằng **Preny Token** là có thể sử dụng ngay.

```bash
export PRENY_TOKEN="your-token-here"
```

## Tag Màu Hệ Thống

| Màu | Ý nghĩa |
|-----|---------|
| ⚪ WHITE | Mới - Chưa phân loại |
| 🟡 YELLOW | Đang quan tâm - Cần chăm sóc |
| 🟢 GREEN | Đã chốt - Khách hàng tiềm năng |
| 🔴 RED | Khó - Cần chú ý đặc biệt |
