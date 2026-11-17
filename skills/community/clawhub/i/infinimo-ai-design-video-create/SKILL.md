---
name: infinimo-ai-design-video-create
description: Generate AI video via Infinimo AI Design—first/last frame, free-form assets, or prompt-only modes; dictionary, credit estimate, uploads, and result polling. Use for text-to-video, image-to-video, and frame-to-frame video.
---

# Video Generation

## About Infinimo AI Design

Infinimo AI Design is an AI design platform for e-commerce visuals. This skill calls the general video generation API (same as `/video-create` in the design studio).

**Web page**: https://design.infinimo.ai/?source=q-i-d-clawhub

## Authentication & base URL

- **Base URL**: `https://www.clawec.com/api`
- **Token**: https://design.infinimo.ai/?source=q-i-d-clawhub (sign up) · https://design.infinimo.ai/api-key?source=q-i-d-clawhub (API Key)
- **Headers**: `Token: <TOKEN>`, `Content-Type: application/json`

Use `INFINIMO_TOKEN` or `INFINIMO_API_KEY`. Common params: `platform=1`, `terminal=4`, `language=en`.

---

## End-to-end flow

```
1. GET  /aigc/ec_media/video/create/dic         → models / ratios / sizes / lengths
2. POST /aigc/ec_media/video/point_calculate    → credit estimate (optional)
3. POST /upload/image or /upload/file           → upload assets
4. POST /aigc/ec_media/video/create             → submit job
5. GET  /aigc/ec_media/video/create/logs        → poll results
```

WebSocket `wss://www.clawec.com/api/aigc/socket` may push `video_result_refresh`.

---

## 1. Dictionary

`GET /aigc/ec_media/video/create/dic`

| Field | Description |
|-------|-------------|
| models | Video models |
| ratios | Aspect ratios |
| sizes | Resolutions |
| lengths | Durations in seconds (`length` submit value is numeric) |

```bash
bash scripts/dic.sh
```

---

## 2. Credit estimate (optional)

`POST /aigc/ec_media/video/point_calculate`

| Parameter | Required | Description |
|-----------|----------|-------------|
| create_mode | yes | `1` / `2` / `3` |
| model, ratio, size | yes | Dictionary ids |
| length | no | Duration (number) |
| prompt | no | Placeholder `.` is fine |

```bash
bash scripts/point_calculate.sh --mode 1 --model M_ID --ratio R_ID --size S_ID --length 5
```

---

## 3. Upload assets

| Mode | Endpoint | Notes |
|------|----------|-------|
| 1 — First/last frame | `POST /upload/image` | First frame required; last optional |
| 2 — Free assets | `POST /upload/file` | Image/video/audio, max 12 |
| 3 — Prompt only | — | No uploads |

```bash
bash scripts/upload_image.sh /path/to/frame.jpg
bash scripts/upload_file.sh /path/to/clip.mp4
```

---

## 4. Submit video generation

`POST /aigc/ec_media/video/create`

| Parameter | Required | Description |
|-----------|----------|-------------|
| prompt | yes | Prompt / script |
| create_mode | yes | `1` first-last / `2` assets / `3` prompt-only |
| model, ratio, size | yes | Dictionary ids |
| length | no | Duration (number) |
| attaches | conditional | Asset URL array (see mode rules) |

### create_mode rules

| Mode | attaches | Rule |
|------|----------|------|
| 1 | `[firstUrl, lastUrl?]` | First frame required |
| 2 | Asset URLs | Max 12 |
| 3 | omit | Prompt only |

```bash
bash scripts/create.sh \
  --mode 1 \
  --prompt "Slow product rotation, studio lighting" \
  --model M_ID --ratio R_ID --size S_ID --length 5 \
  --attaches '["https://cdn.../first.jpg","https://cdn.../last.jpg"]'
```

---

## 5. Poll results

`GET /aigc/ec_media/video/create/logs?start=1&size=5`

| items field | Description |
|-------------|-------------|
| url | Output video URL |
| param | Original submit params |
| time | Created at |

```bash
bash scripts/logs.sh 1 5
```

Delete: `GET /aigc/ec_media/video/log/delete?id=<id>`

See [references/response-schema.md](references/response-schema.md).

---

## Workflow

1. Confirm mode and prompt
2. **dic** → pick options
3. Upload assets if needed
4. Optional **point_calculate** for credits
5. **create** → poll **logs**
6. Return video URL and summary
