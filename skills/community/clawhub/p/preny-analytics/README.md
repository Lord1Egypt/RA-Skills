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

👉 **Không cần đọc báo cáo thủ công**

👉 **Chỉ cần hỏi bằng ngôn ngữ tự nhiên, AI sẽ trả lời ngay**

## Ví dụ câu hỏi

| Câu hỏi | Kết quả |
|---------|---------|
| "Hôm qua có bao nhiêu khách mới?" | Số lượng khách hàng mới |
| "Tỷ lệ chốt đơn tuần này thế nào?" | Hiệu quả chốt đơn |
| "Tag nào mang lại nhiều khách nhất?" | Phân tích theo tag |
| "Có bao nhiêu khách không phản hồi trong 3 ngày qua?" | Trạng thái tương tác |
| "Thống kê tag màu" | Phân loại hệ thống |
| "Thống kê hôm nay" | Báo cáo ngày |

## Phù hợp cho

- 👔 **Chủ shop / sale** cần xem nhanh hiệu quả
- 📊 **Manager** cần số liệu để ra quyết định
- 💬 **Team CSKH** muốn theo dõi chất lượng tương tác

## Tag Màu Hệ Thống (System Tags)

| Màu | Ý nghĩa |
|-----|---------|
| ⚪ WHITE | Mới - Chưa phân loại |
| 🟡 YELLOW | Đang quan tâm - Cần chăm sóc |
| 🟢 GREEN | Đã chốt - Khách hàng tiềm năng |
| 🔴 RED | Khó - Cần chú ý đặc biệt |

## 🚀 Cài đặt nhanh

### Lấy Token từ Preny

1. Đăng nhập vào **https://app.preny.ai**
2. Mở **DevTools** (phím F12 hoặc Cmd+Option+I)
3. Chuyển sang tab **Network**
4. Thao tác bất kỳ trên dashboard
5. Tìm request có header `Authorization: Bearer xxx...`
6. Copy token

### Cấu hình

```bash
export PRENY_TOKEN="your-token-here"
```

**Chỉ cần token là có thể sử dụng ngay!**

## 🔒 Bảo mật

- **KHÔNG** chia sẻ token với người khác
- **KHÔNG** commit token vào git repository
- Token có quyền truy cập dữ liệu doanh nghiệp của bạn

## 📞 Support

- Preny: https://preny.ai
- OpenClaw: https://openclaw.ai
