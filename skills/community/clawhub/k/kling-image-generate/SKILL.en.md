---
name: kling-image-generate
description: Kling AI Image Generation API tool. Supports text-to-image, image-to-image, multi-image reference generation, Omni-Image, image expansion, and more. Uses environment variables KLING_ACCESS_KEY and KLING_SECRET_KEY for authentication. Use this skill when users need AI image generation, image editing, or image extension tasks.
---

# Kling Image Generation

> [🇨🇳 中文](SKILL.md) | **🇬🇧 English**

Kling AI image generation service providing text-to-image, image-to-image, expansion, and various image generation and editing capabilities.

> 🔒 **Security Note**: This skill requires calling the Kling AI official API (`api-beijing.klingai.com`) and uses user-provided API Keys for JWT authentication. All credentials are stored only in local environment variables and will not be uploaded or shared.

## Quick Start

### 1. Configure Environment Variables

```bash
export KLING_ACCESS_KEY="your_access_key"
export KLING_SECRET_KEY="your_secret_key"
```

### 2. Run Scripts

```bash
# Text-to-Image (recommended with progress)
python3 scripts/generate_image_with_progress.py \
  --prompt "A cute cat, Pixar style" \
  --model kling-v3 \
  --n 2 \
  --aspect_ratio 1:1 \
  --wait

# Image-to-Image
python3 scripts/generate_image_with_progress.py \
  --prompt "Keep original style, add flower decorations" \
  --image "https://example.com/image.png" \
  --image_reference subject \
  --wait
```

## Script Overview

| Script | Purpose | Recommendation |
|--------|---------|----------------|
| `generate_image_with_progress.py` | Image generation (with progress display) | ⭐ Recommended |
| `generate_image.py` | Image generation (basic version) | Optional |
| `generate_omni_image.py` | Omni multi-image generation | As needed |
| `expand_image.py` | Image expansion | As needed |
| `query_task.py` | Query task status | Utility |
| `list_tasks.py` | Get task list | Utility |

## Core Features

### Text-to-Image

```bash
python3 scripts/generate_image_with_progress.py \
  --prompt "Describe the image you want" \
  --model kling-v3 \
  --n 1 \
  --aspect_ratio 1:1 \
  --resolution 2k \
  --wait
```

**Common Parameters:**
- `--model`: Model name (kling-v3, kling-v2-1, kling-v1-5, etc.)
- `--n`: Number of images to generate (1-9)
- `--aspect_ratio`: 1:1, 16:9, 9:16, 4:3, etc.
- `--resolution`: 1k, 2k
- `--wait`: Wait for task completion and display progress

### Image-to-Image

```bash
python3 scripts/generate_image_with_progress.py \
  --prompt "Description based on reference image" \
  --image "https://example.com/ref.jpg" \
  --image_reference subject \
  --image_fidelity 0.7 \
  --wait
```

**Reference Types:**
- `subject`: Subject reference (keep person/object identity)
- `face`: Face reference (keep facial features)

### Omni Multi-Image Generation

Supports multi-image reference, style transfer, and other advanced features:

```bash
python3 scripts/generate_omni_image.py \
  --prompt "Apply <<<image_1>>> style to <<<image_2>>>" \
  --images "url1,url2" \
  --model kling-v3-omni \
  --resolution 2k \
  --wait
```

### Image Expansion

Intelligently expand image boundaries:

```bash
# Manual expansion ratios
python3 scripts/expand_image.py \
  --image "https://example.com/img.jpg" \
  --up 0.5 --down 0.5 --left 0.5 --right 0.5 \
  --prompt "Description of expanded area" \
  --wait

# Auto-calculate ratios
python3 scripts/expand_image.py \
  --image "https://example.com/img.jpg" \
  --auto_ratio \
  --width 1024 --height 1024 \
  --aspect_ratio 16:9 \
  --wait
```

## Task Management

### Query Task Status

```bash
python3 scripts/query_task.py --task_id "xxx"
```

### Get Task List

```bash
python3 scripts/list_tasks.py --api_type generation --page 1
```

## Detailed Reference

- **Complete API Parameters**: See [references/api-reference.en.md](references/api-reference.en.md)
- **中文版文档**: [SKILL.md](SKILL.md)
