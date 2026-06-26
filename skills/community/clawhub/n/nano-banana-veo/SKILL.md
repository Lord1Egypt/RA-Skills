---
name: nano-banana-veo
description: Generate images with Nano Banana (Gemini 3 Pro Image) and animate them into videos with Veo 3.1. Use when creating AI-generated visual assets for websites, landing pages, or marketing materials that need both static images and animated video content. Requires GEMINI_API_KEY environment variable.
---

# Nano Banana + Veo Workflow

Generate premium images and animate them into cinematic videos using Google's Gemini API.

## Quick Start

```bash
# Generate just an image
uv run {baseDir}/scripts/generate.py \
  --image-prompt "iPhone floating against dark background, premium product photography" \
  --output-image hero.png

# Generate image + video
uv run {baseDir}/scripts/generate.py \
  --image-prompt "iPhone floating against dark background, premium product photography" \
  --video-prompt "iPhone gently rotating and floating, smooth seamless motion, cinematic lighting" \
  --output-image hero.png \
  --output-video hero.mp4 \
  --video-duration 4
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--image-prompt` | ✅ | - | Prompt for image generation |
| `--video-prompt` | ❌ | image-prompt | Prompt for video animation |
| `--output-image` | ✅ | - | Output path for image (.png/.jpg) |
| `--output-video` | ❌ | - | Output path for video (.mp4) |
| `--resolution` | ❌ | 1K | Image resolution: 1K, 2K, 4K |
| `--video-duration` | ❌ | 4 | Video seconds (4-8, Veo requirement) |
| `--video-resolution` | ❌ | 720p | Video quality: 720p, 1080p, 4k |

## Prerequisites

- `GEMINI_API_KEY` environment variable set
- `google-genai` and `requests` Python packages

## Installation

```bash
# Install dependencies
pip install google-genai requests

# Or with uv
uv pip install google-genai requests
```

## Workflow Examples

### Hero Section Asset
```bash
uv run {baseDir}/scripts/generate.py \
  --image-prompt "Sleek iPhone 15 Pro showing Islamic prayer app interface, dark green and gold accents, floating against pure black background, dramatic studio lighting, premium product photography, 8K quality" \
  --video-prompt "iPhone floating and gently rotating in space, subtle purple glow, smooth seamless boomerang motion, premium cinematic lighting, dark background" \
  --output-image namazlock-hero.png \
  --output-video namazlock-hero.mp4 \
  --video-duration 4
```

### Feature Showcase
```bash
uv run {baseDir}/scripts/generate.py \
  --image-prompt "Minimalist smartphone displaying prayer time interface, clean UI, dark mode with gold accents, studio lighting" \
  --output-image feature.png \
  --resolution 2K
```

## Output

- Images are saved in PNG format
- Videos are saved in MP4 format (H.264 encoded)
- Veo generation takes ~30-60 seconds (async polling handled automatically)

## Notes

- Veo 3.1 requires 4-8 second duration (enforced by API)
- Video generation is asynchronous — script handles polling automatically
- Use `{baseDir}` placeholder in paths — it resolves to the skill directory
