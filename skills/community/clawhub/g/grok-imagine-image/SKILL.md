---
name: xai-image-gen
description: "Generate images with xAI Grok Imagine models — batch generation, aspect ratios, base64 output, concurrent requests. Use when user wants AI image generation via xAI API."
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - XAI_API_KEY
      bins:
        - curl
    primaryEnv: XAI_API_KEY
    emoji: "🎨"
    homepage: https://docs.x.ai/developers/model-capabilities/images/generation
---

# xAI Image Generation

Generate images from text with Grok Imagine models. Supports batch, aspect ratio, resolution, base64, and concurrent requests.

## When to Use

- User asks to generate an image
- User wants AI art or visuals
- User needs batch image generation
- User wants images for social media, marketing, or content

## Quick Start

```bash
curl -X POST https://api.x.ai/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{
    "model": "grok-imagine-image-quality",
    "prompt": "A futuristic city skyline at night"
  }'
```

## Models

| Model | Status | Use Case |
|-------|--------|----------|
| `grok-imagine-image-quality` | ✅ Current | All new requests |
| `grok-imagine-image-pro` | ⚠️ Deprecated May 2026 | Legacy, migrate to quality |

## Parameters

- `prompt` (required) — Text description
- `model` (required) — `grok-imagine-image-quality`
- `n` (optional) — Number of images (1-4)
- `response_format` (optional) — `url` (default) or `b64_json`

## Examples

### Single Image
```bash
curl -X POST https://api.x.ai/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{
    "model": "grok-imagine-image-quality",
    "prompt": "A collage of London landmarks in stenciled street-art style"
  }'
```

### Multiple Variations
```bash
curl -X POST https://api.x.ai/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{
    "model": "grok-imagine-image-quality",
    "prompt": "A futuristic city skyline at night",
    "n": 4
  }'
```

### Base64 Output
```bash
curl -X POST https://api.x.ai/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{
    "model": "grok-imagine-image-quality",
    "prompt": "A serene Japanese garden",
    "response_format": "b64_json"
  }'
```

## Response Format

```json
{
  "data": [
    {
      "url": "https://...",
      "b64_json": "..."
    }
  ]
}
```

## Python SDK

```python
import xai_sdk

client = xai_sdk.Client()
response = client.image.sample(
    prompt="A futuristic city skyline",
    model="grok-imagine-image-quality",
)
print(response.url)
```

## OpenAI SDK Compatible

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.x.ai/v1",
    api_key="YOUR_XAI_API_KEY",
)

response = client.images.generate(
    model="grok-imagine-image-quality",
    prompt="A futuristic city skyline",
)
print(response.data[0].url)
```

## Tips

- URLs are temporary — download promptly
- Use `b64_json` for embedding
- Use `n` parameter for batch variations
- Use async for concurrent different prompts
- Check `respect_moderation` for content filtering
