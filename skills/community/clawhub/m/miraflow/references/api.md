# Miraflow API Reference

Base URL: `https://miraflow.ai/api`
Auth header: `x-api-key: $MIRAFLOW_API_KEY`

## Endpoints

### List Resources

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/avatars` | List available avatars (stock + account) |
| GET | `/api/voices` | List available voices (stock + account) |
| GET | `/api/videos` | List completed videos |
| GET | `/api/video/{id}` | Fetch metadata + downloadUrl for a video |
| GET | `/api/video/{id}/download` | Download video as mp4 binary |
| GET | `/api/video/{id}/status` | Poll job status |
| GET | `/api/image/{jobId}` | Poll image job status |

---

## Create Avatar Video

**POST** `/api/video/create`

Two modes: voice+script or uploaded audio.

### With voice and script (JSON):
```json
{
  "avatarId": "cm2yaz9j10008l0qg9npyjgs3",
  "name": "My video",
  "voiceId": "1",
  "text": "Script text here.",
  "im2vid_full": true
}
```

### With uploaded audio (multipart/form-data):
Fields: `avatarId`, `name`, `mediaId` (from media upload workflow)

### Response:
```json
{ "result": "success", "jobId": "cm42ab3ou0008aggajj0jy5e2" }
```

Then poll `GET /api/video/{jobId}/status` until `inference_complete`.

---

## Video Job Status

**GET** `/api/video/{id}/status`

```json
{
  "result": "success",
  "status": "inference_working",
  "progress": "45%"
}
```

Statuses: `inference_started` | `inference_working` | `inference_complete` | `inference_failed` | `inference_error`

---

## AI Image Generation

**POST** `/api/image/generate`

```json
{
  "prompt": "A photorealistic portrait with natural lighting",
  "name": "My image",
  "aspectRatio": "1:1",
  "negativePrompt": "blurry, low quality",
  "seed": 12345
}
```

Aspect ratios: `1:1` | `16:9` | `9:16` | `4:3` | `3:4`

Response: `{ "result": "success", "jobId": "..." }`
Poll: `GET /api/image/{jobId}`

---

## AI Image Editing

**POST** `/api/image/edit`

```json
{
  "referenceImageMediaId": "cm42ab3ou0008aggajj0jy5e1",
  "prompt": "Turn this into a professional headshot",
  "name": "My edit",
  "aspectRatio": "1:1",
  "negativePrompt": "blurry",
  "seed": 12345
}
```

Multi-image: use `referenceImageMediaIds: ["id1", "id2"]` instead.
Supports multipart/form-data with direct file upload.

---

## Media Upload Workflow

Use this to upload an image for editing or an audio file for avatar video.

### Step 1 – Initialize
**POST** `/api/media/initialize`
```json
{
  "fileName": "image.png",
  "contentType": "image/png",
  "fileSize": 1024000
}
```
Response: `{ "mediaId": "...", "uploadUrl": "https://s3.amazonaws.com/..." }`

### Step 2 – Upload to S3
```bash
curl -X PUT -H "Content-Type: image/png" --data-binary @image.png "$uploadUrl"
```

### Step 3 – Finalize
**POST** `/api/media/finalize`
```json
{ "mediaId": "cm42ab3ou0008aggajj0jy5e2" }
```
Response: `{ "success": true }`

Then use `mediaId` in other API calls.

---

## Image Inpainting

**POST** `/api/image/inpaint`

Requires original image + mask (black=keep, white=replace) + prompt.
Use multipart/form-data or mediaIds.

Fields: `originalImageMediaId`, `maskImageMediaId`, `prompt`, `name`, `aspectRatio`, `negativePrompt`, `seed`

---

## Notes

- Videos are async: always poll status after creation
- `im2vid_full: true` enables full-body avatar animation (photo avatars)
- `downloadUrl` in video metadata is a signed S3 URL (24h TTL)
- Image jobs also return `downloadUrl` when complete via the status endpoint
