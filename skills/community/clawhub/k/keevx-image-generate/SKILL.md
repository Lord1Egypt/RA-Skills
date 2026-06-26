---
name: keevx-image-generate
description: "Use the Keevx API to generate images from prompts and reference images. Supports standard and professional modes, multiple quality levels (1K/2K/4K), various aspect ratios, and batch generation. Use this skill when the user needs to: (1) Generate images from text prompts (2) Create AI images with reference images (3) Batch image generation (4) Query image generation task status. Keywords: image generate, Keevx, AI image, text to image."
---

# Keevx Image Generate Skill

Generate high-quality AI images via the Keevx API using text prompts and optional reference images. Each request generates one or more images with configurable quality, ratio, and mode.

## Prerequisites

Set the environment variable `KEEVX_API_KEY`, obtained from https://www.keevx.com/main/home. Documentation: https://docs.keevx.com

```bash
export KEEVX_API_KEY="your_api_key_here"
```

## API Endpoints

- Base URL: `https://api.keevx.com/v1`
- Upload image: `POST /figure-resource/upload/file` (Content-Type: `multipart/form-data`)
- Create task: `POST /image_generate` (Content-Type: `application/json`)
- Query status: `GET /image_generate/{task_id}`
- Auth: All endpoints use `Authorization: Bearer $KEEVX_API_KEY`
- Source identifier: All endpoints require the `source: skill` Header

## Request Parameters

- `prompt` (required): Generation prompt, max 1000 characters
- `reference_images` (optional): Array of reference image URLs, max 5 images, each under 20MB. Supported formats: JPG/JPEG/PNG/BMP/WebP/GIF
- `module` (optional): Generation mode, `std` (standard, default) or `pro` (professional)
- `generate_count` (optional): Number of images to generate, 1-8, default 1. Each image produces a separate task ID
- `image_quality` (optional): Output quality: `1K`, `2K` (default), `4K`
- `image_ratio` (optional): Aspect ratio, default `9:16`. Valid values: `1:1`, `3:2`, `2:3`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`
- `callback_url` (optional): Callback URL for task completion notification

## Image Input Handling

User-provided images may be URLs or local file paths, handle accordingly:

- **URL** (starts with `http://` or `https://`): Use directly in `reference_images`
- **Local file path**: Upload via the upload endpoint first, then use the returned URL

### Upload Local File

```bash
curl --location 'https://api.keevx.com/v1/figure-resource/upload/file' \
  --header 'Authorization: Bearer $KEEVX_API_KEY' \
  --header 'source: skill' \
  --form 'file=@"/path/to/local/image.png"'
```

Response:

```json
{
  "code": 0,
  "success": true,
  "message": { "global": "success" },
  "result": {
    "url": "https://storage.googleapis.com/.../image.png",
    "fileId": "c5a4676a-...",
    "fileName": "image.png"
  }
}
```

Extract the image URL from `result.url` for use in `reference_images`. For multiple local files, upload each one and collect all URLs.

## Quick Examples

### Basic Generation (Prompt Only)

```bash
curl -X POST "https://api.keevx.com/v1/image_generate" \
  -H "Authorization: Bearer $KEEVX_API_KEY" \
  -H "source: skill" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A serene mountain lake at sunset with golden light reflecting on the water",
    "image_quality": "2K",
    "image_ratio": "16:9"
  }'
```

### Generation with Reference Images

```bash
curl -X POST "https://api.keevx.com/v1/image_generate" \
  -H "Authorization: Bearer $KEEVX_API_KEY" \
  -H "source: skill" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Product shot on white background with soft lighting",
    "reference_images": ["https://example.com/product.jpg"],
    "module": "pro",
    "generate_count": 4,
    "image_quality": "4K",
    "image_ratio": "1:1"
  }'
```

### Query Task Status

```bash
curl -X GET "https://api.keevx.com/v1/image_generate/i2is-xxxxxxxx" \
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
    "task_ids": ["i2is-a1b2c3d4e5f6", "i2is-g7h8i9j0k1l2"]
  }
}
```

The `task_ids` array contains one ID per generated image (count equals `generate_count`). Query each ID individually.

### Task Query - Generating

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "task_id": "i2is-a1b2c3d4e5f6",
    "status": "GENERATING",
    "image_url": "",
    "thumbnail_url": "",
    "error_message": ""
  }
}
```

### Task Query - Succeeded

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "task_id": "i2is-a1b2c3d4e5f6",
    "status": "SUCCEEDED",
    "image_url": "https://storage.googleapis.com/.../image.png",
    "thumbnail_url": "https://storage.googleapis.com/.../thumb.webp",
    "error_message": ""
  }
}
```

### Task Query - Failed

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "task_id": "i2is-a1b2c3d4e5f6",
    "status": "FAILED",
    "image_url": "",
    "thumbnail_url": "",
    "error_message": "Image generation failed due to content policy"
  }
}
```

### Status Values

- `GENERATING`: Task is in progress
- `SUCCEEDED`: Image generated successfully
- `FAILED`: Generation failed, check `error_message`

### Error Response

```json
{
  "code": 100001,
  "msg": "Parameter error: prompt is required"
}
```

## Callback Notification

Provide `callback_url` when creating a task. The system will send a POST request to that URL upon task completion:

```json
{
  "code": 0,
  "msg": "ok",
  "task_type": "image_generate",
  "data": {
    "task_id": "i2is-18e830d27ea041658e4accd576ea7008",
    "status": "SUCCEEDED",
    "image_url": "https://storage.googleapis.com/.../image.png",
    "error_message": ""
  }
}
```

Callback field descriptions:
- `code`: Status code, 0 indicates success
- `task_type`: Fixed as `image_generate`
- `data.task_id`: Task ID
- `data.status`: `SUCCEEDED` or `FAILED`
- `data.image_url`: Generated image URL (on success)
- `data.error_message`: Error message (on failure)

## Polling Strategy

Image generation typically completes within a few minutes. Recommended: 10-second intervals, max 60 retries (up to 10 minutes). If timeout is reached, direct the user to https://www.keevx.com/main/meta/creations to retrieve the result.

```bash
MAX_RETRIES=60
INTERVAL=10

for i in $(seq 1 $MAX_RETRIES); do
  status=$(curl -s -X GET "$API_BASE/image_generate/$TASK_ID" \
    -H "Authorization: Bearer $KEEVX_API_KEY" \
    -H "source: skill" | jq -r '.data.status')

  if [ "$status" = "SUCCEEDED" ]; then echo "Success"; break
  elif [ "$status" = "FAILED" ]; then echo "Failed"; break; fi

  sleep $INTERVAL
done

echo "Maximum wait time (10 minutes) reached. The task may still be processing."
echo "Please visit https://www.keevx.com/main/meta/creations to check and retrieve the result."
```

When `generate_count > 1`, poll each `task_id` from the response individually.

## Error Codes

| HTTP Status Code | Description |
|-----------------|-------------|
| 200 | Success |
| 400 | Parameter error |
| 401 | Authentication failed |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

| Business Error Code | Description | Solution |
|--------------------|-------------|----------|
| 100001 | Parameter error | Check parameter format and required fields |
| 100002 | Validation failed | Verify parameter values are within valid ranges |
| 530002 | Image processing error | Ensure image URL is accessible, format supported, size under 20MB |
| 530003 | Task creation failed | Retry the request |
| 110002 | Task not found | Verify task_id is correct |

## Notes

- Generated image URLs are retained for **7 days** only; download promptly
- Max reference image size: 20MB per image, supported formats: JPG/JPEG/PNG/BMP/WebP/GIF
- Max prompt length: 1000 characters
- Reference images exceeding 5 will be silently truncated to 5
- Images over 15MB are automatically compressed to WebP before processing
- Prompt tips: describe subject, style, composition, lighting, mood, and color palette for best results
