# Playwright Service Skill

Dùng khi cần: chụp screenshot web, lấy tiêu đề trang, scrape nội dung text/HTML.

## Endpoint

```
http://192.168.0.9:3000
```

---

## 1. Screenshot

Chụp ảnh một trang web và gửi vào Telegram.

```bash
curl -s -X POST http://192.168.0.9:3000/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","fullPage":false}' \
  -o /root/.openclaw/workspace/screenshot.jpg
```

- `fullPage: true` → chụp toàn bộ trang (dài)
- `fullPage: false` → chụp viewport 1280x800 (mặc định)

Sau khi có file, gửi vào Telegram group:
```
message tool: action=send, filePath=/root/.openclaw/workspace/screenshot.jpg, channel=telegram, target=-1003778746127
```

---

## 2. Lấy tiêu đề trang

```bash
curl -s -X POST http://192.168.0.9:3000/title \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

Response: `{"url":"...","title":"..."}`

---

## 3. Scrape nội dung

```bash
# Toàn bộ text
curl -s -X POST http://192.168.0.9:3000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'

# Theo CSS selector
curl -s -X POST http://192.168.0.9:3000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","selector":"h1"}'
```

Response: `{"url":"...","data":"..."}`

---

## Lưu ý

- Facebook, Instagram yêu cầu đăng nhập → sẽ trả về trang login, không có nội dung thật
- Trang SPA/React có thể cần thêm thời gian load — nếu scrape ra rỗng, báo Bé Heo để thêm `waitForSelector`
- File screenshot lưu tại `/root/.openclaw/workspace/` trước khi gửi Telegram
