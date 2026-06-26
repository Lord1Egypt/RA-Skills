---
name: news-summary
description: "Tổng hợp tin tức từ Báo Mới, VnExpress, Tuổi Trẻ, Dân Trí — gửi qua Telegram với link bài viết. Dùng khi: tổng hợp tin tức hàng ngày, setup bot tin tức Telegram, cần tin tức Việt Nam nhanh và có link."
---

# News Summary Bot 📰

Tổng hợp tin tức Việt Nam từ 4 nguồn uy tín, gửi qua **Telegram Channel** với link bài viết. Mỗi tin nhấn vào là ra bài gốc.

## Preview

```
📊 TỔNG HỢP TIN TỨC v2 — 08:00 22/03/2026

📰 Báo Mới
  • Iran nã tên lửa đạn đạo vào căn cứ Mỹ [LINK]
  • Lý do Hà Giang, Hội An lọt top điểm đến đẹp [LINK]
  • ...

📰 VnExpress
  • Tin thị trường chứng khoán hôm nay [LINK]
  • ...

📰 Tuổi Trẻ
  • ...

📰 Dân Trí
  • ...
━━━━━━━━━━━━━━━━━━━━━━
✅ Cập nhật lúc 08:00 22/03/2026
🔗 Nhấn vào tin để đọc bài gốc
```

---

## Cách hoạt động

```
news_summary_v2.py (cron 8h, 12h, 16h)
  ├── scrape_baomoi_v2.js  → Báo Mới (Playwright, lấy title + URL)
  ├── RSS: vnexpress.net   → VnExpress (lấy title + URL)
  ├── RSS: tuoitre.vn      → Tuổi Trẻ (lấy title + URL)
  └── RSS: dantri.com.vn   → Dân Trí (lấy title + URL)
  ↓
  Build HTML message với text_link entities
  ↓
  Gửi Telegram → Channel của bạn
```

---

## Các file

| File | Mục đích |
|------|----------|
| `scripts/news_summary_v2.py` | Script chính bằng Python |
| `scripts/news_summary_v2.sh` | Wrapper shell (gọi Python) |
| `scripts/scrape_baomoi_v2.js` | Crawl Báo Mới bằng Playwright |
| `scripts/install.sh` | Setup script — cài đặt nhanh |
| `scripts/config.json.example` | File cấu hình mẫu |
| `config.json` | Cấu hình: bot token, channel |
| `logs/` | Log chạy tự động |

---

## Setup nhanh (1 phút)

```bash
# 1. Clone/copy thư mục news-summary
cd ~/workspace/skills/news-summary/scripts

# 2. Tạo config.json
cp ../config.json.example config.json
# Sửa BOT_TOKEN và CHAT_ID trong config.json

# 3. Test
python3 news_summary_v2.py
```

### 1. Tạo bot Telegram
- Mở **@BotFather** → `/newbot` → đặt tên → lấy **BOT_TOKEN**

### 2. Tạo Channel
- Tạo **Channel Telegram** mới
- Thêm bot làm **Admin** (quyền Post Messages)
- Gửi tin nhắn vào channel → lấy **CHAT_ID**:
  ```
  https://api.telegram.org/bot<TOKEN>/getUpdates
  ```
  Tìm `chat.id` trong response (format: `-100xxxxxxxx`)

### 3. Cấu hình

```json
// config.json (đặt trong thư mục scripts/)
{
  "botToken": "YOUR_BOT_TOKEN_HERE",
  "chatId": "YOUR_CHANNEL_ID_HERE"
}
```

### 4. Cài cron

```bash
crontab -e
# Thêm dòng (giờ VN = UTC+7):
0 8,12,16 * * * cd /home/YOUR_USER/workspace/skills/news-summary/scripts && python3 news_summary_v2.py >> /home/YOUR_USER/.openclaw/logs/news_summary.log 2>&1
```

### 5. Dependencies

```bash
# Python 3 (có sẵn trên hầu hết Linux)
python3 --version

# Playwright (chỉ cần cho Báo Mới)
npm install playwright
npx playwright install chromium
```

---

## Thêm nguồn mới

Trong `news_summary_v2.py`, thêm vào function `main()`:

```python
tt_results = fetch_rss('https://thanhnien.vn/rss/home.rss', 5)
sections.append(build_section('Thanh Niên', tt_results))
```

---

## Troubleshooting

| Lỗi | Cách fix |
|------|---------|
| `playwright timeout` khi lấy Báo Mới | `npx playwright install chromium` |
| Bot không gửi vào channel | Bot cần quyền Admin trong channel |
| `CHAT_ID` sai | Format đúng: `-100xxxxxxxx` |
| Cron không chạy | `tail ~/.openclaw/logs/news_summary.log` |
| Không tìm thấy `config.json` | Đặt trong thư mục `scripts/` |

---

## So sánh v1 vs v2

| Tính năng | v1 | v2 |
|-----------|-----|-----|
| Báo Mới | ✅ | ✅ |
| VnExpress | ✅ | ✅ |
| Tuổi Trẻ | ✅ | ✅ |
| Dân Trí | ✅ | ✅ |
| **Link bài viết** | ❌ | ✅ |
| **Nhấn đọc bài gốc** | ❌ | ✅ |
| Debug log | ❌ | ✅ |
| Chạy độc lập | ❌ | ✅ |

---

## Source

- **Created**: 2026-03-21
- **Version**: 2.0 (có link bài viết)
- **Skill ID**: news-summary-v2
