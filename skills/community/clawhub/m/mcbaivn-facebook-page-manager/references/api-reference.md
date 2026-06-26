# API Reference - Facebook Page Manager

## Endpoints dùng trong skill

| Tính năng | Method | Endpoint |
|-----------|--------|----------|
| Đăng text | POST | `/{page-id}/feed` |
| Đăng ảnh | POST | `/{page-id}/photos` |
| Carousel | POST | `/{page-id}/feed` (với `attached_media`) |
| Video/Reels | POST | `/{page-id}/videos` |
| Story ảnh | POST | `/{page-id}/photo_stories` |
| Story video | POST | `/{page-id}/video_stories` |
| Scheduled posts | GET | `/{page-id}/scheduled_posts` |
| Xóa bài | DELETE | `/{post-id}` |
| Sửa scheduled | POST | `/{post-id}` |
| Comment vào bài | POST | `/{post-id}/comments` |
| Reply vào comment | POST | `/{comment-id}/comments` |
| Xem comments | GET | `/{post-id}/comments` |
| Xóa comment | DELETE | `/{comment-id}` |

---

## Hẹn giờ đăng bài

`scheduled_publish_time` phải là **Unix timestamp** và phải:
- Trong tương lai ít nhất **10 phút**
- Không quá **6 tháng** từ hiện tại

Kèm theo `"published": "false"` trong request.

Ví dụ Python:
```python
from datetime import datetime
ts = int(datetime(2024, 12, 25, 8, 0).timestamp())
```

---

## Carousel

Upload từng ảnh với `published=false` → lấy photo ID → gộp vào feed post:

```json
{
  "message": "Caption đây",
  "attached_media": [
    {"media_fbid": "photo_id_1"},
    {"media_fbid": "photo_id_2"},
    {"media_fbid": "photo_id_3"}
  ]
}
```

---

## Video/Reels

- Format: MP4 (H.264 video, AAC audio)
- Reels: thêm `"video_type": "REELS"`
- Max size: 10GB, max duration: 240 phút
- Reels: 3-90 giây

---

## Story

- Photo story: JPEG/PNG, ratio 9:16 khuyến nghị
- Video story: MP4, max 15 giây
- **Không hỗ trợ schedule** — đăng ngay

---

## Graph API Version

Skill dùng `v19.0`. Kiểm tra version mới nhất tại:
https://developers.facebook.com/docs/graph-api/changelog
