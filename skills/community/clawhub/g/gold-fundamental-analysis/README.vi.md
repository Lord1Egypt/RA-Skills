# 📊 Gold Fundamental Analysis — Phân Tích Cơ Bản Vàng

**Phân tích cơ bản cho Vàng (XAU/USD)** — Dữ liệu vĩ mô, COT positioning, ETF flows, Fed stance & lịch kinh tế.

<p align="center">
  <a href="https://clawhub.ai/skills/gold-fundamental-analysis"><img src="https://img.shields.io/badge/clawhub-skill-blue" alt="ClawHub"></a>
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

**[🇺🇸 English](README.md)**

---

## 📖 Giới thiệu

**Gold Fundamental Analysis** fetch và phân tích dữ liệu cơ bản của Vàng từ **5 nguồn dữ liệu uy tín**, đưa ra báo cáo có cấu trúc với các yếu tố Bullish/Bearish, điểm số định lượng (-100 đến +100) và triển vọng ngắn/trung/dài hạn.

Được thiết kế cho **OpenClaw agents** — dùng cả on-demand lẫn trong cron jobs cho các phiên giao dịch hàng ngày (Á/Âu/Mỹ).

> ⚠️ **Disclaimer:** Đây là công cụ **phân tích bổ trợ**, không phải lời khuyên tài chính. Đầu tư có rủi ro.

## ✨ Nguồn dữ liệu

| # | Nguồn | Dữ liệu | Độ tin cậy |
|---|-------|---------|-----------|
| 1 | **FRED API** (Fed St. Louis) | Lãi suất, CPI, Lợi suất 10Y, Real yield, DXY | ⭐⭐⭐⭐⭐ |
| 2 | **CFTC COT** | Managed Money long/short, net position | ⭐⭐⭐⭐⭐ |
| 3 | **SPDR Gold ETF (SSGA/GLD)** | AUM, NAV, lượng vàng ước tính | ⭐⭐⭐⭐ |
| 4 | **Fed RSS** | Thông báo chính sách tiền tệ (30 ngày) | ⭐⭐⭐⭐⭐ |
| 5 | **ForexFactory** | Sự kiện kinh tế USD tác động cao/trung bình | ⭐⭐⭐⭐ |

## 📊 7 Trụ cột phân tích

| # | Trụ cột | Tín hiệu | Tác động |
|---|---------|---------|----------|
| 1 | **Fed Policy** | Ôn hoà → +Bullish / Diều hâu → −Bearish | ⭐⭐⭐⭐⭐ |
| 2 | **Inflation** | Tăng → +Bullish (vàng là kênh phòng hộ) | ⭐⭐⭐⭐ |
| 3 | **Real Yield** | Giảm → +Bullish / Tăng → −Bearish | ⭐⭐⭐⭐⭐ |
| 4 | **DXY** | Yếu → +Bullish / Mạnh → −Bearish | ⭐⭐⭐⭐⭐ |
| 5 | **ETF Flows** | Vào ròng → +Bullish / Ra ròng → −Bearish | ⭐⭐⭐ |
| 6 | **COT** | Short cực đoan → contrarian +Bullish / Long cực đoan → contrarian −Bearish | ⭐⭐⭐⭐ |
| 7 | **Sự kiện sắp tới** | FOMC/CPI/NFP trong 3 ngày → biến động tăng | ⭐⭐⭐ |

## 🚀 Cài đặt

```bash
pip install requests
git clone https://github.com/kimminhpro/gold-fundamental-analysis-skill.git
cd gold-fundamental-analysis-skill
python3 scripts/get_gold_fundamental_data.py
```

## 🔧 Sử dụng

```bash
# Cơ bản
python3 scripts/get_gold_fundamental_data.py

# Custom FRED key
python3 scripts/get_gold_fundamental_data.py --fred-key KEY_CUA_BAN

# Hoặc dùng biến môi trường
FRED_API_KEY=key_cua_ban python3 scripts/get_gold_fundamental_data.py
```

Chi tiết xem [README.md](README.md) tiếng Anh.

## ⚠️ Cảnh báo

- ❌ Không phải lời khuyên tài chính
- ❌ Không cam kết lợi nhuận
- ✅ Luôn dùng stop loss
- ✅ Tự chịu trách nhiệm
