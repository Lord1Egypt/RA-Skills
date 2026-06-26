# WeChat Cover Photo Generation with Seedream 5.0 API

This document explains how to generate professional WeChat Official Account cover photos (21:9 aspect ratio) using the Doubao Seedream 5.0 API.

## Overview

The `generate_cover_photo.py` script uses Doubao's Seedream 5.0 API (火山方舟) to automatically generate high-quality cover photos for WeChat articles based on article title and theme.

## Prerequisites

1. **Seedream API Key**: Configure in `~/.openclaw/credentials/seedream.json`
2. **Python 3.7+** with `requests` library
3. **PIL/Pillow** for image resizing: `pip install Pillow`

## API Configuration

- **Endpoint**: `https://ark.cn-beijing.volces.com/api/v3/images/generations`
- **Authentication**: Bearer token (API key)
- **Model**: `doubao-seedream-5-0-260128`
- **Default Size**: `1536x1024` (2K resolution)
- **Default Aspect Ratio**: `3:2` (then cropped to 21:9 for WeChat)

## Supported Sizes

- Generation: `1536x1024` (recommended), `1024x1024`, etc.
- Final Output: `900x386` (21:9, WeChat standard)

## Usage

```bash
# Basic usage
python scripts/generate_cover_photo.py \
  --title "你的AI每天晚上都在做梦" \
  --theme "OpenClaw 4月大版本更新" \
  --output "output/cover.png"

# With custom style
python scripts/generate_cover_photo.py \
  --title "文章标题" \
  --theme "主题" \
  --style "flat vector illustration" \
  --color-scheme "blue gradient" \
  --output "output/cover.png"

# Skip resize (keep original size)
python scripts/generate_cover_photo.py \
  --title "标题" \
  --theme "主题" \
  --output "output/cover.png" \
  --no-resize
```

## Credentials File

Create `~/.openclaw/credentials/seedream.json`:

```json
{
  "api_key": "your-api-key",
  "endpoint": "https://ark.cn-beijing.volces.com/api/v3/images/generations",
  "model": "doubao-seedream-5-0-260128",
  "default_size": "1536x1024",
  "default_aspect_ratio": "3:2"
}
```

## Fallback: GLM-Image API

If Seedream is unavailable, use GLM-Image API:

```bash
python scripts/generate_cover_photo.py \
  --use-glm \
  --glm-api-key "your-glm-key" \
  --title "标题" \
  --theme "主题" \
  --output "output/cover.png"
```
