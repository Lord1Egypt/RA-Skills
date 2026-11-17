---
name: infinimo-ai-design-product-video-create
description: Create handheld product short videos via Infinimo AI Design—avatar first-frame compositing, AI script writing, image-to-video submit and polling. Use for shoppable shorts, avatar-led product demos, and listing promo video.
---

# Handheld Product Video

## About Infinimo AI Design

Infinimo AI Design is an AI design platform for e-commerce visuals. This skill covers **Handheld product video** (avatar-led product shorts)—same as `/product-video-create` in the design studio.

**Web page**: https://design.infinimo.ai/?source=q-i-d-clawhub

## Authentication & base URL

- **Base URL**: `https://www.clawec.com/api`
- **Token**: https://design.infinimo.ai/?source=q-i-d-clawhub · https://design.infinimo.ai/api-key?source=q-i-d-clawhub
- **Headers**: `Token: <TOKEN>`

Use `INFINIMO_TOKEN` or `INFINIMO_API_KEY`. Common params: `platform=1`, `terminal=4`, `language=en`.

---

## Three-step wizard flow

```
Step 1  Avatar first frame
  GET  /aigc/ec_product_video/image/create/avatar_options  → avatar list
  GET  /aigc/ec_product_video/image/create/dic             → first-frame dictionary
  POST /upload/image                                       → product photo (max 1)
  POST /aigc/ec_product_video/image/create                 → generate first-frame candidates
  WebSocket product_video_image_result_refresh             → candidate URLs

Step 2  Pick first-frame URL for video

Step 3  Video generation
  GET  /aigc/ec_product_video/video/create/dic             → video dictionary
  POST /aigc/ec_media/video/point_calculate                → credit estimate
  POST /aigc/ec_product_video/text_create (optional)       → AI script
  POST /upload/image (optional)                            → manual first/last frame
  POST /aigc/ec_product_video/video/create                 → submit video
  GET  /aigc/ec_product_video/video/create/logs            → poll results
```

WebSocket events: `product_video_image_result_refresh` (first frames), `video_result_refresh` (video).

---

## Step 1: Avatar first frame

### 1.1 Avatar list

`GET /aigc/ec_product_video/image/create/avatar_options`

Optional filters: `gender`, `race`. Items include `id`, `imageThumb` → use `avatarId` on submit.

```bash
bash scripts/avatar_options.sh 1 10
```

### 1.2 First-frame dictionary

`GET /aigc/ec_product_video/image/create/dic`

```bash
bash scripts/image_dic.sh
```

### 1.3 Upload product photo

`POST /upload/image` — max **1** product reference.

```bash
bash scripts/upload_image.sh /path/to/product.jpg
```

### 1.4 Generate first-frame candidates

`POST /aigc/ec_product_video/image/create`

| Parameter | Required | Description |
|-----------|----------|-------------|
| avatarId | yes | Avatar id |
| model, ratio, size | yes | Dictionary ids (9:16 ratio common) |
| prompt | no | Scene description |
| images | no | Product photo URL array |

```bash
bash scripts/image_create.sh \
  --avatar-id AVATAR_ID \
  --model M_ID --ratio R_ID --size S_ID \
  --images '["https://cdn.../product.jpg"]' \
  --prompt "Handheld product, live-commerce style"
```

WebSocket payload example:

```json
{ "type": "product_video_image_result_refresh", "data": { "images": ["url1", "url2"] } }
```

Pick one URL as `attaches[0]` for the video step.

---

## Step 3: Video generation

### 3.1 Video dictionary

`GET /aigc/ec_product_video/video/create/dic`

```bash
bash scripts/video_dic.sh
```

### 3.2 Credit estimate

`POST /aigc/ec_media/video/point_calculate` with `create_mode=1`

```bash
bash scripts/point_calculate.sh --model M_ID --ratio R_ID --size S_ID --length 10
```

### 3.3 AI script (optional)

`GET /aigc/ec_product_video/text_model/options` → text models

`POST /aigc/ec_product_video/text_create`

| Parameter | Description |
|-----------|-------------|
| prompt | Creative brief |
| model | Text model id |
| target_language | e.g. `English`, `简体中文` |
| video_length | 5–15 seconds |

```bash
bash scripts/text_create.sh \
  --prompt "Wireless earbuds shoppable voiceover" \
  --model TEXT_MODEL_ID \
  --lang English \
  --length 10
```

Use returned script as video `prompt`.

### 3.4 Submit video

`POST /aigc/ec_product_video/video/create`

| Parameter | Required | Description |
|-----------|----------|-------------|
| prompt | yes | Script / prompt |
| create_mode | yes | Always `1` (first-last frame) |
| model, ratio, size | yes | Dictionary ids |
| length | no | Duration (number) |
| attaches | yes | `[firstFrameUrl, lastFrameUrl?]` — first required |

```bash
bash scripts/video_create.sh \
  --prompt "Voiceover script..." \
  --model M_ID --ratio R_ID --size S_ID --length 10 \
  --attaches '["https://cdn.../first_frame.jpg"]'
```

### 3.5 Poll results

`GET /aigc/ec_product_video/video/create/logs?start=1&size=5`

```bash
bash scripts/video_logs.sh 1 5
```

Delete: `GET /aigc/ec_product_video/video/log/delete?id=<id>`

See [references/response-schema.md](references/response-schema.md).

---

## Workflow

1. Pick avatar + upload product → generate first-frame candidates → select frame
2. Optional AI script or user-provided prompt
3. Pick video model/ratio/duration → submit → poll logs
4. Return video URL and parameter summary
