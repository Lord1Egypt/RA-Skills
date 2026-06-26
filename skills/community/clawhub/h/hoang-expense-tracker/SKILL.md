---
name: expense-tracker
description: Trợ lý tài chính cá nhân đa năng. Dùng khi user muốn GHI NHẬN CHI TIÊU (nay ăn hết 50k, đổ xăng 50k...), XEM BÁO CÁO (vẽ biểu đồ chi tiêu), ĐẶT NGÂN SÁCH (budget tháng này), hoặc NHỜ CHỬI (roast cách tiêu tiền).
---

# AI Personal CFO

Skill này là một trợ lý tài chính xịn xò. Hãy xác định nhu cầu của user và dùng tool `exec` gọi script tương ứng.

## 1. Ghi nhận chi tiêu (Log Expense)
- Trích xuất số tiền (`amount`), danh mục (`category` - tiếng Anh: Food, Drink, Transport, Shopping, Other), và mô tả (`desc`).
- Gọi: `python3 /home/hoang/.openclaw/workspace/expense-tracker/scripts/finance_manager.py log --amount <tiền> --category <nhóm> --desc "<mô tả>"`
- Phản hồi user xác nhận.

## 2. Báo cáo (Report & Chart)
- Khi user bảo "Báo cáo chi tiêu", "Vẽ biểu đồ", "Tổng kết".
- Gọi: `python3 /home/hoang/.openclaw/workspace/expense-tracker/scripts/finance_manager.py report`
- Script sẽ trả về đường dẫn `chart_path` tới ảnh PNG.
- Phản hồi: Dùng tool `message` để gửi ảnh đó lại cho user (kèm theo lời giải thích ngắn gọn).

## 3. Khẩu nghiệp / Tư vấn (Roast & Advise)
- Khi user bảo "Chửi tao đi", "Nhận xét cách tiêu tiền", "Roast me".
- Gọi: `python3 /home/hoang/.openclaw/workspace/expense-tracker/scripts/finance_manager.py roast`
- Phản hồi: Chế giễu cách tiêu tiền một cách vui vẻ hoặc khuyên răn dựa trên output của script.

## 4. Đặt ngân sách (Budget)
- Khi user bảo "Đặt ngân sách Food 2 triệu".
- Gọi: `python3 /home/hoang/.openclaw/workspace/expense-tracker/scripts/finance_manager.py budget --amount 2000000 --category "Food"`
- Phản hồi xác nhận.