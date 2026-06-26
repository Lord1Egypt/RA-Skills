---
name: minimax-image-generator
description: Text-to-image and image-to-image generation using MiniMax API. Generates images from text prompts (t2i) or transforms reference images (i2i) using MiniMax's image-01 or image-01-live models.
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      env:
        - MINIMAX_API_KEY
      bins:
        - python3
    primaryEnv: MINIMAX_API_KEY
---

# MiniMax Image Generation (Text-to-Image & Image-to-Image)

> ⚠️ Requires a **Coding Plan API Key**
> Subscribe at: [https://platform.minimaxi.com/subscribe/coding-plan](https://platform.minimaxi.com/subscribe/coding-plan)

Text-to-image (t2i) and image-to-image (i2i) generation tool using MiniMax's image generation API.

---

## Setup

### 1. Configure API Key

```bash
openclaw config set skills.entries.minimax-image-generator.apiKey "sk-your-key"
```

Or add to `openclaw.json` skills entries:

```json
{
  "skills": {
    "entries": {
      "minimax-image-generator": {
        "apiKey": "sk-your-key"
      }
    }
  }
}
```

### 2. Dependencies

```bash
pip install requests
```

---

## Architecture

```
~/.openclaw/workspace/skills/minimax-image-generator/
├── SKILL.md
├── _meta.json
└── scripts/
    └── minimax_image_gen.py
```

---

## Usage

### From terminal

```bash
# Text-to-image (t2i) - basic
MINIMAX_API_KEY="sk-your-key" python3 scripts/minimax_image_gen.py "a beautiful sunset over ocean"

# Text-to-image with options
MINIMAX_API_KEY="sk-your-key" python3 scripts/minimax_image_gen.py "a cat" --model image-01 --aspect-ratio 16:9 --n 2

# Image-to-image (i2i) - reference image by URL
MINIMAX_API_KEY="sk-your-key" python3 scripts/minimax_image_gen.py "transform to anime style" --image-url "https://example.com/photo.jpg"

# Image-to-image with base64
MINIMAX_API_KEY="sk-your-key" python3 scripts/minimax_image_gen.py "make it brighter" --image-base64 "data:image/jpeg;base64,..."

# Save to file
MINIMAX_API_KEY="sk-your-key" python3 scripts/minimax_image_gen.py "a cat" --save cat.png
```

### From code

```python
from minimax_image_gen import generate_image

# Text-to-image
result = generate_image(
    prompt="a beautiful sunset over ocean",
    model="image-01",
    aspect_ratio="16:9",
    n=1
)

# Image-to-image (URL)
result = generate_image(
    prompt="transform to anime style",
    image_url="https://example.com/photo.jpg"
)

# Image-to-image (base64)
result = generate_image(
    prompt="make it brighter",
    image_base64="data:image/jpeg;base64,..."
)
```

---

## Tool Definition

**Name:** `minimax_image_gen`

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "prompt": {
      "type": "string",
      "description": "Image description text, max 1500 chars."
    },
    "model": {
      "type": "string",
      "enum": ["image-01", "image-01-live"],
      "default": "image-01",
      "description": "Model name."
    },
    "image_url": {
      "type": "string",
      "description": "Reference image URL for image-to-image (i2i). Supports public URLs."
    },
    "image_base64": {
      "type": "string",
      "description": "Reference image as base64 Data URL for i2i. Format: data:image/jpeg;base64,..."
    },
    "aspect_ratio": {
      "type": "string",
      "enum": ["1:1", "16:9", "4:3", "3:2", "2:3", "3:4", "9:16", "21:9"],
      "default": "1:1",
      "description": "Image aspect ratio."
    },
    "style_type": {
      "type": "string",
      "enum": ["漫画", "元气", "中世纪", "水彩"],
      "description": "Style (only for image-01-live)."
    },
    "n": {
      "type": "integer",
      "minimum": 1,
      "maximum": 9,
      "default": 1,
      "description": "Number of images to generate."
    },
    "response_format": {
      "type": "string",
      "enum": ["url", "base64"],
      "default": "url",
      "description": "Return format."
    },
    "prompt_optimizer": {
      "type": "boolean",
      "default": false,
      "description": "Enable prompt auto-optimization."
    }
  },
  "required": ["prompt"]
}
```

**Output:** JSON with image URLs or base64 data

---

## Error Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1002 | Rate limit |
| 1004 | Auth failed - check API Key |
| 1008 | Insufficient balance |
| 1026 | Content violation |
| 2013 | Parameter error |
| 2049 | Invalid API Key |
