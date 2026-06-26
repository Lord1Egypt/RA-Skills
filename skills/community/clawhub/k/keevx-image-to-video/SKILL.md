---
name: keevx-image-to-video
description: Use the Keevx API to convert images to videos. Supports multiple models (V/KL), various resolutions (720p/1080p/4K), and audio generation. Use this skill when the user needs to: (1) Convert images to video (2) Generate video with Keevx (3) Create and query image-to-video tasks (4) Batch image-to-video conversion. Keywords: image to video, Keevx, video generation.
---

# Keevx Image-to-Video Skill

Convert images to high-quality videos via the Keevx API.

## Prerequisites

Set the environment variable `KEEVX_API_KEY`, obtained from https://www.keevx.com/main/home. Documentation: https://docs.keevx.com

```bash
export KEEVX_API_KEY="your_api_key_here"
```

## API Endpoints

- Base URL: `https://api.keevx.com/v1`
- Upload image: `POST /figure-resource/upload/file` (Content-Type: `multipart/form-data`)
- Create task: `POST /image_to_video` (Content-Type: `application/json`)
- Query status: `GET /image_to_video/{task_id}`
- Auth: All endpoints use `Authorization: Bearer $KEEVX_API_KEY`
- Source identifier: All endpoints require the `source: skill` Header

## Model Selection

| Parameter | Model V (General, Recommended) | Model KL (Multi-Reference) |
|-----------|------|--------|
| prompt | ✅ Required, max 1000 chars | ✅ Required |
| image_url | Required for single-image mode, max 20MB | ❌ Not supported |
| reference_images | Required for multi-image mode, max 3 images, each max 20MB | ✅ Required, max 7 images, each max 20MB |
| aspect_ratio | ✅ 16:9 / 9:16 | ✅ 16:9 / 9:16 |
| aspect_resolution | 720p / 1080p / 4k | 720p / 1080p |
| duration | Single-image: 4/6/8s, Multi-image: fixed 8s | 5 / 10s |
| generate_audio | ✅ Supported, default false | ❌ Not supported |
| generate_count | Optional 1-4 | Optional 1-4 |
| callback_url | Optional | Optional |

### Model Selection Guide

- **Choose Model V**: When audio is needed, 4K resolution required, single or multi-image input, high quality requirements
- **Choose Model KL**: When multiple reference images are available (2-7), multi-angle showcase needed, product demo videos

### Model-Specific Request Bodies

#### Model V

```json
{
  "model": "V",
  "prompt": "Video description (required, max 1000 chars)",
  "image_url": "https://... (required for single-image mode)",
  "reference_images": ["https://..."],
  "aspect_ratio": "16:9",
  "aspect_resolution": "720p | 1080p | 4k",
  "duration": 4,
  "generate_audio": true,
  "generate_count": 1
}
```

#### Model KL

```json
{
  "model": "KL",
  "prompt": "Video description (required)",
  "reference_images": ["https://..."],
  "aspect_ratio": "16:9",
  "aspect_resolution": "720p | 1080p",
  "duration": 5,
  "generate_count": 1
}
```

## Image Input Handling

User-provided images may be URLs or local file paths, handle accordingly:

- **URL** (starts with `http://` or `https://`): Use directly as `image_url` or `reference_images`
- **Local file path**: Upload via the upload endpoint first, then use the returned URL

### Upload Local File

```bash
curl --location 'https://api.keevx.com/v1/figure-resource/upload/file' \
  --header 'Authorization: Bearer $KEEVX_API_KEY' \
  --header 'source: skill' \
  --form 'file=@"/path/to/local/image.png"'
```

Response example:

```json
{
  "code": 0,
  "success": true,
  "message": { "global": "success" },
  "result": {
    "url": "https://storage.googleapis.com/..../image.png",
    "fileId": "c5a4676a-...",
    "fileName": "image.png"
  }
}
```

Extract the image URL from `result.url` for use as `image_url` or `reference_images`. For multiple local files, upload each one and collect all URLs.

## Quick Examples

### Single Image Generation (Model V)

```bash
curl -X POST "https://api.keevx.com/v1/image_to_video" \
  -H "Authorization: Bearer $KEEVX_API_KEY" \
  -H "source: skill" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "V",
    "prompt": "Waves crashing on the beach at sunset",
    "image_url": "https://example.com/beach.jpg",
    "aspect_ratio": "16:9",
    "aspect_resolution": "1080p",
    "duration": 6,
    "generate_audio": true
  }'
```

### Multi-Reference Image Generation (Model KL)

```bash
curl -X POST "https://api.keevx.com/v1/image_to_video" \
  -H "Authorization: Bearer $KEEVX_API_KEY" \
  -H "source: skill" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "KL",
    "prompt": "City night timelapse, neon lights flickering",
    "reference_images": [
      "https://example.com/city1.jpg",
      "https://example.com/city2.jpg",
      "https://example.com/city3.jpg"
    ],
    "aspect_ratio": "16:9",
    "aspect_resolution": "1080p",
    "duration": 10,
    "generate_count": 2
  }'
```

### Query Task Status

```bash
curl -X GET "https://api.keevx.com/v1/image_to_video/i2v-xxxxxxxx" \
  -H "Authorization: Bearer $KEEVX_API_KEY" \
  -H "source: skill"
```

## Response Format

### Task Created Successfully

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "task_ids": ["i2v-d6b6472bcf724d0399e06d1390cb964e"]
  }
}
```

### Task Query Success

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "task_id": "i2v-d6b6472bcf724d0399e06d1390cb964e",
    "status": "SUCCEEDED",
    "video_url": "https://storage.googleapis.com/.../sample_0.mp4",
    "thumbnail_url": "https://storage.googleapis.com/.../thumbnail.webp",
    "error_message": "",
    "duration": 6,
    "width": 1920,
    "height": 1080
  }
}
```

### Status Values

`PENDING` (queued) / `PROCESSING` (in progress) / `SUCCEEDED` (completed) / `FAILED` (failed)

### Failure Response

```json
{
  "code": 100001,
  "msg": "Parameter error: prompt cannot be empty"
}
```

## Callback Notification

Provide `callback_url` when creating a task. The system will send a POST request to that URL upon task completion:

```json
{
  "code": 0,
  "msg": "ok",
  "task_type": "image_to_video",
  "data": {
    "task_id": "i2v-d6b6472bcf724d0399e06d1390cb964e",
    "status": "SUCCEEDED",
    "video_url": "https://storage.googleapis.com/.../sample_0.mp4",
    "thumbnail_url": "https://storage.googleapis.com/.../thumbnail.webp",
    "error_message": ""
  }
}
```

## Polling Strategy

Video generation may take up to 20 minutes. Recommended: 30-second intervals, max 40 retries.

```bash
MAX_RETRIES=40
INTERVAL=30

for i in $(seq 1 $MAX_RETRIES); do
  status=$(curl -s -X GET "$API_BASE/image_to_video/$TASK_ID" \
    -H "Authorization: Bearer $KEEVX_API_KEY" \
    -H "source: skill" | jq -r '.data.status')

  if [ "$status" = "SUCCEEDED" ]; then echo "Success"; break
  elif [ "$status" = "FAILED" ]; then echo "Failed"; break; fi

  sleep $INTERVAL
done
```

## Error Codes

| HTTP Status Code | Description |
|-----------------|-------------|
| 200 | Success |
| 400 | Parameter error |
| 401 | Authentication failed |
| 404 | Resource not found |
| 413 | Request body too large |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

| Business Error Code | Description | Solution |
|--------------------|-------------|----------|
| 100001 | Parameter error | Check parameter format and required fields |
| 100002 | Invalid token | Verify API Key is correct and active |
| 100003 | Task not found | Verify task_id is correct |
| 100004 | Image size exceeded | Compress image to under 20MB |
| 100005 | Prompt too long | Shorten prompt to within 1000 characters |
| 100006 | Image URL inaccessible | Ensure image URL is publicly accessible |
| 100007 | Unsupported image format | Use common formats such as JPG, PNG |

## Notes

- Generated video/thumbnail URLs are retained for **7 days** only; download promptly
- Max image size: 20MB, supported formats: JPG/PNG/WebP
- Max prompt length: 1000 characters
- 429 error: retry after 30s; 500 error: retry after 10s; network error: retry immediately, max 3 times
- Prompt tips: describe subject, scene, action, mood; include visual details (lighting, color, texture)
- Narration script: to add narration to the video, use `Speak "narration content"` in the prompt, e.g. `Speak "Welcome to our channel"`
- Image tips: use high-resolution, subject-focused, evenly-lit, well-composed images
