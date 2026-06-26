---
name: nano-banana-2
description: "Generate and edit images using Google's Nano Banana 2 (Imagen) model — the latest high-quality image generation AI. Supports text-to-image generation and image editing with up to 14 reference images. Two provider modes: Atlas Cloud and Google AI Studio. Use this skill whenever the user wants to generate images, create AI art, edit photos with AI, do image-to-image transformation, create illustrations, make visual content, or mentions Nano Banana, Imagen, Gemini image, or Google image generation. Also trigger when users ask to create sprites, thumbnails, banners, logos, product photos, concept art, or any visual asset using AI."
source: "https://github.com/AtlasCloudAI/nano-banana-2-skill"
homepage: "https://github.com/AtlasCloudAI/nano-banana-2-skill"
metadata:
  openclaw:
    requires:
      env:
        - ATLASCLOUD_API_KEY
        - GEMINI_API_KEY
    primaryEnv: ATLASCLOUD_API_KEY
---

# Nano Banana 2 Image Generation

Generate and edit images using Google's Nano Banana 2 (Imagen) model via two provider options.

> **Privacy & data note**: This skill sends text prompts and image data to third-party APIs (Atlas Cloud at `api.atlascloud.ai` or Google AI Studio at `generativelanguage.googleapis.com`) for image generation. For image editing via Atlas Cloud, local files are uploaded to Atlas Cloud's temporary storage to obtain a URL — the agent MUST ask the user for explicit confirmation before uploading any local file. Uploaded files are temporary and may be cleaned up periodically. No data is stored locally beyond the downloaded output files.

## Required Environment Variables

| Variable | Required | Description |
|----------|:--------:|-------------|
| `ATLASCLOUD_API_KEY` | If using Atlas Cloud | Atlas Cloud API key for image generation |
| `GEMINI_API_KEY` | If using Google AI Studio | Google AI Studio API key |

At least one of the above must be set. If both are set, ask the user which provider to use.

## Provider Selection

1. If `ATLASCLOUD_API_KEY` is set → use Atlas Cloud
2. If `GEMINI_API_KEY` is set → use Google AI Studio
3. If both are set → ask the user which provider to use
4. If neither is set → ask the user to configure one:
   - **Atlas Cloud**: Sign up at https://www.atlascloud.ai, Console → API Keys → Create key, then `export ATLASCLOUD_API_KEY="your-key"`
   - **Google AI Studio**: Get key from https://aistudio.google.com/apikey, then `export GEMINI_API_KEY="your-key"`

**Atlas Cloud**
- Async API with polling workflow
- Flat-rate pricing regardless of resolution
- Supports 300+ models through one API key

**Google AI Studio**
- Direct access via Google's Gemini API
- Synchronous response with base64 image output

## Pricing Comparison

| Resolution | Google AI Studio | Atlas Cloud | Savings |
|:----------:|:----------------:|:-----------:|:-------:|
| **1K** (default) | $0.080/image | **$0.072/image** | 10% off |
| **2K** | $0.080/image | **$0.072/image** | 10% off |
| **4K** | $0.080/image | **$0.072/image** | 10% off |

Atlas Cloud is 10% cheaper than Google AI Studio across all resolutions, with flat-rate pricing regardless of resolution.

## Available Models

### Text-to-Image Models
| Model ID (Atlas Cloud) | Price | Description |
|------------------------|-------|-------------|
| `google/nano-banana-2/text-to-image` | $0.072/image | Stable, production-ready |

### Image Editing Models
| Model ID (Atlas Cloud) | Price | Description |
|------------------------|-------|-------------|
| `google/nano-banana-2/edit` | $0.072/image | Stable image editing |

Google AI Studio model: `gemini-3.1-flash-image-preview` (handles both generation and editing)

---

## Mode 1: Atlas Cloud API

### Setup
The user needs an Atlas Cloud API key. Guide them to:
1. Sign up at https://www.atlascloud.ai
2. Go to Console → API Keys → Create new key
3. Set environment variable: `export ATLASCLOUD_API_KEY="your-key"`

### Script Usage

This skill includes a Python script for image generation. Zero external dependencies required.

#### List available image models

```bash
python scripts/generate_image.py list-models
```

#### Generate an image

```bash
python scripts/generate_image.py generate \
  --model "MODEL_ID" \
  --prompt "Your prompt here" \
  --output ./output
```

#### Upload a local image (for editing)

```bash
python scripts/generate_image.py upload ./local-image.jpg
```

#### Edit an image

```bash
python scripts/generate_image.py generate \
  --model "MODEL_ID" \
  --prompt "Edit instruction" \
  --image "https://...uploaded-url..."
```

Run `python scripts/generate_image.py generate --help` for all options. Extra model params can be passed as key=value (e.g. `aspect_ratio=16:9 resolution=2k`).

---

### Text-to-Image Generation

**Parameters:**

| Parameter | Type | Required | Default | Options |
|-----------|------|----------|---------|---------|
| `prompt` | string | Yes | - | Text description of the image |
| `aspect_ratio` | string | No | 1:1 | 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 |
| `resolution` | string | No | 1k | 1k, 2k, 4k |
| `output_format` | string | No | png | png, jpeg |
| `seed` | integer | No | random | For reproducible results |

**Workflow — submit, poll, download:**

```bash
# Step 1: Submit generation request
curl -s -X POST "https://api.atlascloud.ai/api/v1/model/generateImage" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/nano-banana-2/text-to-image",
    "prompt": "A serene Japanese garden with cherry blossoms",
    "aspect_ratio": "16:9",
    "resolution": "2k"
  }'
# Response: { "code": 0, "data": { "id": "prediction-id" } }

# Step 2: Poll for result (repeat until status is "completed" or "succeeded")
curl -s "https://api.atlascloud.ai/api/v1/model/prediction/{prediction-id}" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY"
# Response when done: { "code": 0, "data": { "status": "completed", "outputs": ["https://...image-url..."] } }

# Step 3: Download the image
curl -o output.png "IMAGE_URL_FROM_OUTPUTS"
```

When implementing this workflow programmatically:
- Poll every 2-3 seconds
- Check for status: "completed" or "succeeded" means done
- Check for status: "failed" means error — read the `error` field
- Image URLs are in `data.outputs[]` array

### Uploading Local Images

To use local images for editing, first upload them to get a URL. The agent MUST confirm with the user before uploading any local file (e.g., "I'll upload `/path/to/image.jpg` to Atlas Cloud for editing. Proceed?").

```bash
curl -s -X POST "https://api.atlascloud.ai/api/v1/model/uploadMedia" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -F "file=@/path/to/local/image.jpg"
# Returns: { "code": 200, "data": { "download_url": "https://...url...", "filename": "image.jpg", "size": 123456 } }
```

Use the returned `download_url` as the image URL in the `images` array for editing requests.

> **Note**: Uploaded files are for temporary use with Atlas Cloud generation tasks only. URLs may expire after a period of time.

### Image Editing

Same workflow as text-to-image, but with additional `images` parameter:

| Parameter | Type | Required | Default | Options |
|-----------|------|----------|---------|---------|
| `prompt` | string | Yes | - | Editing instruction |
| `images` | array of strings | Yes | - | 1-14 image URLs to edit |
| `aspect_ratio` | string | No | - | Same options as above |
| `resolution` | string | No | 1k | 1k, 2k, 4k |

```bash
curl -s -X POST "https://api.atlascloud.ai/api/v1/model/generateImage" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/nano-banana-2/edit",
    "prompt": "Change the sky to a dramatic sunset",
    "images": ["https://example.com/photo.jpg"],
    "resolution": "2k"
  }'
```

### Using Atlas Cloud MCP Tools (if available)

If the user has the Atlas Cloud MCP server configured, use the built-in tools directly:

```
# Quick generate
atlas_quick_generate(model_keyword="nano banana 2", type="Image", prompt="...")

# Or with specific model
atlas_generate_image(model="google/nano-banana-2/text-to-image", params={...})

# Check result
atlas_get_prediction(prediction_id="...")
```

---

## Mode 2: Google AI Studio (Official)

### Setup
1. Get API key from https://aistudio.google.com/apikey
2. Set environment variable: `export GEMINI_API_KEY="your-key"`

### Text-to-Image Generation

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "A serene Japanese garden with cherry blossoms"}]
    }],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "imageConfig": {
        "aspectRatio": "16:9",
        "imageSize": "2K"
      }
    }
  }'
```

**Parameters for Google AI Studio:**

| Parameter | Location | Options |
|-----------|----------|---------|
| `aspectRatio` | `generationConfig.imageConfig` | 1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9 |
| `imageSize` | `generationConfig.imageConfig` | 512px, 1K, 2K, 4K (uppercase K required) |
| `responseModalities` | `generationConfig` | ["TEXT", "IMAGE"] for image output |

**Response handling:**
The response contains base64-encoded image data in `candidates[0].content.parts[]`. Loop through parts — text parts have `.text`, image parts have `.inline_data.mime_type` and `.inline_data.data` (base64).

### Image Editing (Google AI Studio)

Include the source image as base64 inline_data alongside the text prompt:

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [
        {"text": "Change the sky to a dramatic sunset"},
        {"inline_data": {
          "mime_type": "image/png",
          "data": "BASE64_ENCODED_IMAGE"
        }}
      ]
    }],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"]
    }
  }'
```

### Python Example (Google AI Studio)

```python
from google import genai
from google.genai import types
import base64

client = genai.Client()

# Text-to-Image
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents="A serene Japanese garden with cherry blossoms",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="2K"
        ),
    )
)

for part in response.parts:
    if part.text:
        print(part.text)
    elif image := part.as_image():
        image.save("output.png")
```

---

## Implementation Guide

When the user asks to generate an image, follow this workflow:

1. **Determine provider**: Check which API key is available (see Provider Selection above).

2. **Extract parameters from user request**:
   - Prompt: the image description
   - Aspect ratio: infer from context (banner→16:9, portrait→9:16, square→1:1, phone wallpaper→9:16, desktop wallpaper→16:9)
   - Resolution: default 1k unless user wants high quality (then 2k or 4k)
   - For editing: identify source image(s)

3. **Choose model** (Atlas Cloud only):
   - Use `google/nano-banana-2/text-to-image` for generation
   - Use `google/nano-banana-2/edit` for editing tasks

4. **Execute the API call** using bash with curl

5. **For Atlas Cloud**: Poll the prediction endpoint every 3 seconds until complete, then download the image

6. **For Google AI Studio**: Parse the response, extract base64 image data, save to file

7. **Present the result**: Show the saved file path and offer to open it

## Prompt Engineering Tips

Share these with users to get better results:
- Be specific about style: "oil painting", "photorealistic", "anime style", "watercolor"
- Describe lighting: "golden hour", "studio lighting", "neon glow"
- Mention composition: "close-up", "wide angle", "bird's eye view"
- Include mood: "serene", "dramatic", "whimsical"
- For text in images: Nano Banana 2 handles text rendering well — just include the text in quotes in your prompt
