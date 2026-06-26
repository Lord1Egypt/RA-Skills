# Cách lấy Facebook Page Access Token

## Tổng quan

Để dùng Facebook Graph API đăng bài lên Page, cần **Page Access Token** (không phải User Token thông thường).

---

## Bước 1: Tạo Facebook App

1. Vào **[Meta for Developers](https://developers.facebook.com/)**
2. Click **My Apps → Create App**
3. Chọn **"Other"** → **"Business"** → Đặt tên app → Create
4. Vào **App Dashboard** → Ghi lại **App ID** và **App Secret**

---

## Bước 2: Lấy User Access Token tạm thời (để test)

1. Vào **[Graph API Explorer](https://developers.facebook.com/tools/explorer/)**
2. Chọn app của bạn ở dropdown
3. Click **"Generate Access Token"**
4. Chọn permissions:
   - `pages_manage_posts` ✅
   - `pages_read_engagement` ✅
   - `pages_manage_engagement` ✅ (nếu cần)
   - `publish_video` ✅ (nếu đăng video)
5. Click **Generate Token** → Cho phép quyền

> ⚠️ Token này chỉ có hiệu lực **1-2 giờ** — dùng để test thôi!

---

## Bước 3: Lấy Page Access Token

Sau khi có User Token tạm, chạy lệnh sau để lấy danh sách Page và token dài hạn:

```bash
curl "https://graph.facebook.com/v19.0/me/accounts?access_token=USER_TOKEN_CỦA_BẠN"
```

Response sẽ trả về:
```json
{
  "data": [
    {
      "access_token": "EAAxxxxxxxx...",   ← ĐÂY LÀ PAGE TOKEN
      "category": "Media/News Company",
      "name": "Tên Page của bạn",
      "id": "123456789",                  ← PAGE ID
      "tasks": ["ANALYZE", "ADVERTISE", "MODERATE", "CREATE_CONTENT"]
    }
  ]
}
```

Lưu lại `access_token` (Page Token) và `id` (Page ID).

---

## Bước 4: Tạo Long-Lived Page Access Token (không hết hạn)

Page Access Token từ bước 3 thường **không hết hạn** nếu page đã publish và app đã qua review cơ bản.

Để chắc chắn, đổi sang long-lived token:

**Bước 4a:** Đổi User Token ngắn → Long-lived User Token
```bash
curl "https://graph.facebook.com/oauth/access_token
  ?grant_type=fb_exchange_token
  &client_id=APP_ID
  &client_secret=APP_SECRET
  &fb_exchange_token=SHORT_USER_TOKEN"
```

**Bước 4b:** Lấy lại Page Token từ long-lived User Token
```bash
curl "https://graph.facebook.com/v19.0/me/accounts?access_token=LONG_LIVED_USER_TOKEN"
```

Page Token lúc này sẽ **không hết hạn** (never expires).

---

## Bước 5: Kiểm tra token

Dán token vào [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/) để kiểm tra:
- Type: `PAGE`
- Expires: `Never` ✅
- Scopes có đủ permissions không

---

## Bước 6: Lưu config vào `fb_config.json`

Tạo file `fb_config.json` trong cùng thư mục với `fb_post.py`:

```json
{
  "access_token": "EAAxxxxxxxxxxxxxxxxxxxxxxxx",
  "page_id": "123456789012345"
}
```

> 🔒 **QUAN TRỌNG:** Thêm `fb_config.json` vào `.gitignore` — đừng commit token lên GitHub!

---

## Troubleshooting

| Lỗi | Nguyên nhân | Cách fix |
|-----|-------------|----------|
| `(#200) Requires manage_pages permission` | Thiếu permission | Regenerate token với đủ scopes |
| `(#100) Invalid parameter` | Sai page_id hoặc endpoint | Kiểm tra lại page_id |
| `Token expired` | Token hết hạn | Làm lại từ Bước 4 |
| `(#368) The action attempted...` | Page chưa publish hoặc bị hạn chế | Kiểm tra trạng thái Page |
| `Video upload failed` | File quá lớn hoặc sai format | MP4 H.264, max 10GB, dưới 240 phút |

---

## Permissions cần thiết

| Tính năng | Permission |
|-----------|------------|
| Đăng text/ảnh | `pages_manage_posts` |
| Đăng video/Reels | `pages_manage_posts` + `publish_video` |
| Đăng Story | `pages_manage_posts` |
| Xem/xóa bài | `pages_read_engagement` |
| Hẹn giờ đăng | `pages_manage_posts` |

---

## Note về Story

Facebook Graph API hỗ trợ đăng Story qua:
- `/{page-id}/photo_stories` (ảnh)
- `/{page-id}/video_stories` (video)

Story **không hỗ trợ hẹn giờ** qua API — đăng ngay lập tức.
