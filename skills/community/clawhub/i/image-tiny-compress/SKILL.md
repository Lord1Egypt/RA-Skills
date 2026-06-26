---
name: TinyCompress
description: "Compress PNG, JPEG, WebP images using TinyPNG/Tinify free web API. No API key required, no login needed. Supports single/batch/directory compression with automatic retry and rate-limit handling."
version: 1.0.0
metadata:
  openclaw:
    emoji: "🗜️"
    homepage: "https://tinypng.com"
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: requests
---

# TinyCompress — Smart Image Compression

<description>
Use when: compressing images, optimizing image file size, reducing image size, tinypng, tinify, compress image, compress png, compress jpeg, compress webp, image optimization, shrink image, 压缩图片, 图片压缩, 图片优化, 图片瘦身, 减小图片体积
NOT for: image resizing/cropping, format conversion, image editing, video compression
</description>

## Overview

TinyCompress uses TinyPNG/Tinify's free web API to perform high-quality lossy compression on PNG, JPEG, and WebP images. No API key, no login, no payment required.

**Key Features:**
- Free — no API key or registration needed
- Supports PNG, JPEG, WebP formats
- Max 5MB per image, up to 20 images per batch
- Supports global server (tinypng.com) and China server (tinify.cn)
- Auto retry with exponential backoff on failure
- Rate-limit friendly with built-in request delays
- Typical compression: 50%~80% size reduction with near-zero visual quality loss

## Prerequisites

- **Python 3.6+** must be installed
- **requests** library: `pip install requests`
- Network access to `tinypng.com` or `tinify.cn`

## Usage

### 1. Single Image Compression

When a user uploads or specifies one image:

```bash
python "{SKILL_DIR}/scripts/tiny_compress.py" compress "<image_path>"
```

Use China server for faster speed in China:
```bash
python "{SKILL_DIR}/scripts/tiny_compress.py" compress "<image_path>" --server cn
```

Output: generates `<filename>_compressed.<ext>` in the same directory.

### 2. Batch Compression

When a user provides multiple images:

```bash
python "{SKILL_DIR}/scripts/tiny_compress.py" compress "<file1>" "<file2>" ... --output-dir "<output_dir>"
```

### 3. Directory Compression

When a user specifies a directory:

```bash
python "{SKILL_DIR}/scripts/tiny_compress.py" compress-dir "<dir_path>" --output-dir "<output_dir>"
```

Add `--recursive` to include subdirectories.

### 4. Overwrite Mode

When user explicitly wants to replace original files:

```bash
python "{SKILL_DIR}/scripts/tiny_compress.py" compress "<file>" --overwrite
```

⚠️ **Warning:** Overwriting is irreversible. Always warn the user and suggest backup first.

## Script Reference

### scripts/tiny_compress.py

| Subcommand | Description |
|------------|-------------|
| `compress <files...>` | Compress one or more image files |
| `compress-dir <dir>` | Compress all images in a directory |

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--output-dir <dir>` | Output directory | Same dir with `_compressed` suffix |
| `--server cn\|global` | Server selection | `global` |
| `--overwrite` | Overwrite original files | `false` |
| `--recursive` | Recurse into subdirectories (compress-dir only) | `false` |

**How it works:**
- Upload endpoint: `POST https://tinypng.com/backend/opt/shrink` (or `tinify.cn/backend/opt/shrink`)
- Uploads raw image binary → server returns compression info + download URL → downloads compressed image
- Uses randomized User-Agent and X-Forwarded-For headers
- Serial processing with 1.5s delay between requests to avoid rate limiting
- Auto retry up to 3 times with exponential backoff

**Output format (per image):**
```json
{
  "success": true,
  "file": "original_path",
  "output": "output_path",
  "original_size": 1234567,
  "compressed_size": 345678,
  "saved_bytes": 888889,
  "saved_percent": 72.0
}
```

## Examples

```
User: "Compress this image" (uploads photo.png)
Agent: runs compress on photo.png → returns photo_compressed.png with stats

User: "Compress all images in ./screenshots"
Agent: runs compress-dir ./screenshots → returns compressed versions

User: "Use China server, compress these 3 photos"
Agent: runs compress with --server cn on all 3 files
```

## Limitations

- Max 5MB per image (TinyPNG web limit)
- Max 20 images per batch
- This uses TinyPNG's web frontend endpoint (not official API), may change without notice
- High-frequency requests may be temporarily rate-limited
- Does not support AVIF, GIF, BMP formats
- Uploaded images are auto-deleted from TinyPNG servers after 48 hours

## Important Notes

- **Privacy:** Images are uploaded to TinyPNG servers for processing. Do NOT upload images containing sensitive/personal information.
- **Fair Use:** This method simulates web browser access. Use responsibly, avoid excessive automated calls.
- **Network:** Requires access to tinypng.com or tinify.cn.
- **Alternative:** For heavy batch processing, consider registering for TinyPNG's official API key (500 free compressions/month).
