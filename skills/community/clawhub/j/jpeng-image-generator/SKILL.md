---
name: jpeng-image-generator
description: "AI image generation skill using DALL-E, Stable Diffusion, or Midjourney API. Generate, edit, and vary images from text prompts."
version: "1.0.0"
author: "jpeng"
tags: ["image", "ai", "dalle", "stable-diffusion", "generation"]
---

# Image Generator

Generate AI images using DALL-E, Stable Diffusion, or other providers.

## When to Use

- User wants to generate an image from text
- Create variations of existing images
- Edit images with AI inpainting
- Generate thumbnails or illustrations

## Configuration

```bash
# OpenAI DALL-E
export OPENAI_API_KEY="sk-xxx"

# Stability AI
export STABILITY_API_KEY="sk-xxx"

# Replicate (for SDXL, etc.)
export REPLICATE_API_TOKEN="r8_xxx"
```

## Usage

### Generate image

```bash
python3 scripts/generate_image.py \
  --prompt "A serene mountain landscape at sunset" \
  --size "1024x1024" \
  --output "./output.png"
```

### Generate variations

```bash
python3 scripts/generate_image.py \
  --vary "./input.png" \
  --count 4 \
  --output-dir "./variations"
```

### Edit image (inpainting)

```bash
python3 scripts/generate_image.py \
  --edit "./input.png" \
  --mask "./mask.png" \
  --prompt "Add a rainbow in the sky"
```

### With style presets

```bash
python3 scripts/generate_image.py \
  --prompt "A futuristic city" \
  --style "cyberpunk" \
  --negative "blurry, low quality"
```

## Output

```json
{
  "success": true,
  "image_path": "./output.png",
  "revised_prompt": "A serene mountain landscape..."
}
```
