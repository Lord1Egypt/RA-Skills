---
name: vn-stock-scanner
description: Chuyên gia phân tích chứng khoán Việt Nam (VN-Index, HoSE, HNX, UPCoM). Sử dụng để LẤY TIN TỨC CHỨNG KHOÁN (cập nhật CafeF, tin đồn, tin chủ tịch mua/bán, chia cổ tức) hoặc TRA CỨU MÃ CỔ PHIẾU VN (P/E, P/B, EPS, Vốn hóa, Ngành nghề).
---

# VN Stock Scanner

Đây là Agent Skill được thiết kế riêng cho chứng khoán Việt Nam, lấy dữ liệu trực tiếp từ các nguồn uy tín như CafeF và API của công ty chứng khoán (TCBS).

## 1. Tra cứu thông tin mã cổ phiếu (Ticker Info)
Khi user hỏi về một mã chứng khoán (VD: "Phân tích mã FPT", "Chỉ số của VCB thế nào?"):
- Trích xuất mã cổ phiếu (`ticker`): ví dụ `FPT`, `VCB`, `HPG`.
- Sử dụng tool `exec` gọi lệnh:
  ```bash
  python3 /home/hoang/.openclaw/workspace/vn-stock-scanner/scripts/scanner.py ticker --ticker <mã_cổ_phiếu>
  ```
- Dùng thông tin trả về (P/E, P/B, EPS, Tỷ suất cổ tức...) để trả lời user và đưa ra nhận định ngắn gọn.

## 2. Quét tin tức và tin đồn (News & Rumor Scanner)
Khi user hỏi "Có tin tức chứng khoán gì hot không?", "Tìm tin đồn", "Chủ tịch đăng ký mua bán":
- Nhận diện từ khóa user quan tâm (`keywords`). Nếu user muốn tin chung chung thì bỏ trống. Nếu user muốn tin về mua/bán nội bộ, thì truyền `keywords="mua,bán,chủ tịch,đăng ký"`.
- Sử dụng tool `exec` gọi lệnh:
  ```bash
  python3 /home/hoang/.openclaw/workspace/vn-stock-scanner/scripts/scanner.py news --keywords "<từ_khóa>"
  ```
- Lọc các tin tức trả về và định dạng lại gọn gàng để gửi cho user. Đưa ra nhận xét khách quan về tác động của các tin này tới thị trường (Tích cực/Tiêu cực/Trung lập).