---
name: nano-banana-image-gen
description: >-
  Generate and edit images using Pixwith API's Nano Banana 2 model.
  Supports text-to-image and image-to-image (up to 4 reference images).
  Use when the user asks to generate images, edit photos, create AI art,
  text-to-image, or image-to-image with Nano Banana 2.
version: 1.0.1
publisher: Pixwith AI
homepage: https://pixwith.ai
categories:
  - image-generation
  - image-editing

tags:
  - pixwith
  - nano-banana
  - image-generation
  - text-to-image
  - image-to-image

env:
  PIXWITH_API_KEY:
    required: true
    description: Pixwith API key used to authenticate API requests.

permissions:
  network:
    domains:
      - api.pixwith.ai
      - uploads.pixwith.ai
      - "*.amazonaws.com"

  filesystem:
    access: user-provided
    description: >
      May read image files explicitly provided by the user for upload
      when performing image generation or editing tasks.

  persistence:
    modify_agent_config: false
    write_files: false
    
capabilities:
  - check_credits
  - text_to_image
  - image_to_image
  - image_upload
  - task_creation
  - task_status_polling
---

# Pixwith Nano Banana 2 — AI Image Generation

Generate and edit images via the Pixwith API using the Nano Banana 2 model.
Supports text-to-image and image-to-image with up to 4 reference images,
multi-resolution output (1K / 2K / 4K), and flexible aspect ratios.

## ⚠️ CRITICAL — Do NOT Alter API Response Values

**ALL values returned by the API (`task_id`, `result_urls`, `image_url`, `upload_url`, `fields`) are opaque tokens. Use them EXACTLY as returned — do NOT add, remove, or change even a single character.** Store each value in a shell variable and reuse it directly. A single wrong character in `task_id` or `result_urls` will cause errors or broken links.

## Setup

This skill requires a `PIXWITH_API_KEY` environment variable.

**If the variable is not set**, guide the user through these steps:

1. Go to https://pixwith.ai/api and sign up / log in.
2. Click "Add" to create a new API key and copy it.
3. Add the key to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "nano-banana-image-gen": {
        "enabled": true,
        "env": { "PIXWITH_API_KEY": "key_your_key_here" }
      }
    }
  }
}
```

**Verify** by running:

```bash
curl -s -X POST https://api.pixwith.ai/api/task/get_credits \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY"
```

A successful response looks like `{"code":1,"data":{"credits":500}}`.

## Pricing

| Resolution | Credits per image |
|------------|-------------------|
| 1K         | 10                |
| 2K         | 15                |
| 4K         | 20                |

Always inform the user of the cost before creating a task.

## Model Parameters

- **model_id**: `0-41` (fixed)
- **prompt** (required): Describe the image to generate or the edit to apply.
- **image_urls** (optional): 1–4 publicly accessible image URLs for image-to-image mode.
- **options.prompt_optimization** (boolean, default `true`): Auto-translate prompt to English.
- **options.resolution** (required): `1K`, `2K`, or `4K`.
- **options.aspect_ratio** (required): `0` (auto-match input image), `1:1`, `16:9`, `9:16`, `3:4`, `4:3`, `3:2`, `2:3`, `5:4`, `4:5`, `21:9`.

## Workflow A — Text-to-Image

Use when the user provides only a text prompt and no images.

### Step 1: Check credits

```bash
curl -s -X POST https://api.pixwith.ai/api/task/get_credits \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY"
```

Verify `data.credits` is sufficient for the chosen resolution.

### Step 2: Create task

```bash
curl -s -X POST https://api.pixwith.ai/api/task/create \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY" \
  -d '{
    "prompt": "<user_prompt>",
    "model_id": "0-41",
    "options": {
      "prompt_optimization": true,
      "resolution": "1K",
      "aspect_ratio": "1:1"
    }
  }'
```

Response contains `data.task_id` and `data.estimated_time` (seconds).

### Step 3: Poll for results

Wait for `estimated_time` seconds, then poll:

```bash
curl -s -X POST https://api.pixwith.ai/api/task/get \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY" \
  -d '{"task_id": "<task_id>"}'
```

- `data.status == 1` → still processing, wait 5 seconds and poll again.
- `data.status == 2` → done, `data.result_urls` contains the image URLs.
- `data.status == 3` → failed, inform the user.

Present the EXACT `result_urls` to the user.

## Workflow B — Image-to-Image

Use when the user provides one or more reference images plus a text prompt.

### Step 1: Upload local images (if needed)

If the user provides a local file path (not a public URL), upload it first.

**Upload constraints:**

- Allowed formats: `.jpg`, `.jpeg`, `.png` only
- Maximum file size: **10 MB**
- `content_type` must match the file: `image/jpeg` for .jpg/.jpeg, `image/png` for .png
- The presigned upload URL expires in **10 minutes**

**1a. Get a presigned upload URL:**

```bash
curl -s -X POST https://api.pixwith.ai/api/task/pre_url \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY" \
  -d '{"image_name": "photo.jpg", "content_type": "image/jpeg"}'
```

Set `content_type` based on the file extension:
- `.jpg` / `.jpeg` → `"image/jpeg"`
- `.png` → `"image/png"`

Response:
- `data.upload_url` — presigned POST data (`url` + `fields`)
- `data.image_url` — the final CDN URL to use in `image_urls`

**1b. Upload the file using the presigned data:**

```bash
curl -s -X POST "<upload_url.url>" \
  -F "key=<upload_url.fields.key>" \
  -F "Content-Type=<upload_url.fields.Content-Type>" \
  -F "x-amz-credential=<upload_url.fields.x-amz-credential>" \
  -F "x-amz-algorithm=<upload_url.fields.x-amz-algorithm>" \
  -F "x-amz-date=<upload_url.fields.x-amz-date>" \
  -F "x-amz-signature=<upload_url.fields.x-amz-signature>" \
  -F "policy=<upload_url.fields.policy>" \
  -F "file=@/path/to/local/image.jpg"
```

Fill every field from the `upload_url.fields` object into the form.
After upload, use `data.image_url` from step 1a as the image URL.

If the user already has a public image URL (starts with `http`), skip this step.

### Step 2: Check credits

Same as Workflow A, Step 1.

### Step 3: Create task with images

```bash
curl -s -X POST https://api.pixwith.ai/api/task/create \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY" \
  -d '{
    "prompt": "<edit_instruction>",
    "image_urls": ["<image_url_1>", "<image_url_2>"],
    "model_id": "0-41",
    "options": {
      "prompt_optimization": true,
      "resolution": "1K",
      "aspect_ratio": "0"
    }
  }'
```

When editing images, `aspect_ratio: "0"` auto-matches the input image dimensions.

### Step 4: Poll for results

Same as Workflow A, Step 3.

## Error Handling

All API responses follow `{"code": 1, "message": "success", "data": {...}}`.
When `code` is `0`, `message` contains the error. Common errors:

- `Invalid API KEY` — key is missing, wrong, or disabled.
- `Credits not enough` — user needs to purchase more credits at https://pixwith.ai/pricing.
- `Invalid image format` — only jpg, png, jpeg are supported.
- `Invalid image url` — the URL is not publicly accessible.

## Defaults

When the user does not specify preferences, use these defaults:

- resolution: `1K`
- aspect_ratio: `1:1` (text-to-image) or `0` (image-to-image)
- prompt_optimization: `true`
