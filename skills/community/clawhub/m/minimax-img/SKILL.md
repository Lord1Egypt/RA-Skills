---
name: minimax-image
description: Use MiniMax image-01 model to generate images from text prompts. Supports high-quality PNG output, downloaded from Hailuo CDN. Install when needed.
homepage: https://platform.minimax.io
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["python"]}}}
---

# MiniMax Image Generation

Call via: `python scripts/minimax_media.py image "<prompt>"`

## Usage

```bash
# Basic
python scripts/minimax_media.py image "A cute cat"

# Detailed prompt
python scripts/minimax_media.py image "A futuristic city at sunset, cyberpunk style, highly detailed"
```

Returns: `{"image_path": "...", "url": "...", "size_bytes": ...}`

- `image_path`: Local path to saved PNG file
- `url`: Direct CDN URL to the generated image
- `size_bytes`: File size in bytes

## Prompt Tips

- Be specific and descriptive for best results
- Include style keywords (e.g., "photorealistic", "anime", "watercolor")
- Mention lighting, mood, and composition for more controlled output

## Environment

- `MINIMAX_API_KEY` — required
- `MINIMAX_BASE_URL` — optional (default: https://api.minimax.io)

## Example Response

```json
{
  "image_path": "/tmp/tmp123.png",
  "url": "http://hailuo-image-algeng-data-us.oss-us-east-1.aliyuncs.com/...",
  "size_bytes": 245000
}
```
