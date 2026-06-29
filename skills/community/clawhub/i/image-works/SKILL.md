---
slug: image-works
name: Image Workshop / 图片批量处理工坊
version: 1.0.0
author: Golden Bean (coder)
category: Multimedia
description: Batch image processing - compress, resize, format convert, watermark, EXIF clean, and crop. All local, no upload needed.
model: deepseek/deepseek-v4-flash
input_schema: schemas/input.schema.json
output_schema: schemas/output.schema.json
---

# Image Workshop Skill

Local-first batch image processing toolkit. Compress, resize, convert formats, add watermarks, clean EXIF, crop — all on your machine with no image upload. Includes presets for Chinese social platforms (WeChat, Xiaohongshu, Taobao, etc.).

## Core Capabilities

- **Compress**: Quality target, size target, lossless, or auto-smart
- **Resize**: Fixed dimensions, scale ratio, max-edge constraint, batch uniform
- **Convert**: JPEG ↔ PNG ↔ WebP ↔ AVIF ↔ TIFF (bidirectional)
- **Watermark**: Text or image, custom position/opacity, tile mode
- **EXIF**: Remove all metadata, remove GPS only, or view metadata
- **Crop**: Region crop, aspect-ratio crop (1:1, 4:3, 16:9, 3:4)
- **Presets**: One-shot platform-optimized processing (WeChat, Xiaohongshu, Taobao, etc.)

## Chinese Platform Presets

| Platform | Preset Name | Specs |
|----------|------------|-------|
| WeChat Moments | `wechat-moments` | 3×3 grid crop for 9-square layout |
| WeChat Official Account | `wechat-cover` | 900×383px (2.35:1), <10MB |
| Xiaohongshu | `xiaohongshu` | 3:4 ratio, 1080×1440px |
| Taobao Main Image | `taobao-main` | 800×800px (1:1), <500KB |
| Douyin Cover | `douyin-cover` | 1920×1080 (16:9) |
| Weibo Image | `weibo` | 1200px wide, <20MB |
| Bilibili Cover | `bilibili-cover` | 16:9, 1920×1080 |
| Avatar | `avatar` | 400×400 (1:1), <200KB |

## Usage

```
clawhub run image-works --input <paths> --op <operation> --output <dir>
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--input` | json-array | required | File paths, directories, or glob patterns |
| `--op` | json-array | required | Operations to apply (see below) |
| `--preset` | string | — | Platform preset (overrides --op) |
| `--output.dir` | string | `./processed/` | Output directory |
| `--output.suffix` | string | `''` | Filename suffix |
| `--output.overwrite` | bool | false | Overwrite existing files |
| `--output.keep-structure` | bool | true | Preserve original dir structure |
| `--recursive` | bool | false | Scan subdirectories |
| `--max-files` | int | 1000 | Maximum files to process |

### Operations

**Compress**: `{"type":"compress","quality":80,"target_size_kb":500}`
**Resize**: `{"type":"resize","width":1200,"height":900,"fit":"inside"}`
**Convert**: `{"type":"convert","format":"webp","quality":85}`
**Watermark**: `{"type":"watermark","text":"© My Name","position":"bottom-right","opacity":0.5}`
**EXIF**: `{"type":"exif","action":"remove"}`
**Crop**: `{"type":"crop","aspect_ratio":"1:1"}`

Operations are applied in array order.

## Sample Prompts

### 1. Batch compress all JPEGs in a directory (most common)
```text
clawhub run image-works --input './photos/*.jpg' \
  --op '[{"type":"compress","quality":80}]' \
  --output ./compressed/
# → 47 files processed, 156.2MB → 42.8MB (72.6% saved)
```

### 2. Xiaohongshu preset (one-shot)
```text
clawhub run image-works --input ./product-photos/ \
  --preset xiaohongshu \
  --output ./xiaohongshu-ready/
# → Auto-resize to 3:4 (1080×1440), compress, export as JPEG
```

### 3. Add watermark with resize + format conversion
```text
clawhub run image-works --input ./portfolio/ \
  --op '[{"type":"watermark","text":"© My Name","position":"bottom-right","opacity":0.3},{"type":"convert","format":"webp","quality":90}]' \
  --output ./watermarked-webp/
# → Watermarked + WebP converted
```

### 4. EXIF cleanup for privacy-safe sharing
```text
clawhub run image-works --input ./vacation-photos/ \
  --op '[{"type":"exif","action":"remove"}]' \
  --output ./safe-to-share/
# → All GPS/device metadata removed
```

### 5. Batch resize for e-commerce (Taobao main image)
```text
clawhub run image-works --input ./raw-products/ \
  --op '[{"type":"resize","width":800,"height":800,"fit":"cover"},{"type":"compress","quality":85}]' \
  --output ./taobao-ready/
# → Uniform 800×800 product images, optimized
```

## First-Success Path

```
Step 1: Install → clawhub install image-works
Step 2: Run → clawhub run image-works --input ~/Pictures/ --op '{"type":"compress","quality":80}'
Step 3: See space-savings report → immediate value
Step 4: Explore presets → xiaohongshu, wechat-cover, etc.
```

## Core Scripts

| File | Purpose |
|------|---------|
| `scripts/__init__.py` | Package init |
| `scripts/scanner.py` | File scanner (glob, recursive) |
| `scripts/processor.py` | Core processing pipeline |
| `scripts/operations/compress.py` | Quality/target-size/lossless compression |
| `scripts/operations/resize.py` | Dimension resize, fit modes |
| `scripts/operations/convert.py` | Format conversion |
| `scripts/operations/watermark.py` | Text/image/tile watermark |
| `scripts/operations/exif.py` | EXIF read/remove/GPS-only |
| `scripts/operations/crop.py` | Region/aspect-ratio crop |
| `scripts/presets.py` | Platform preset definitions |
| `scripts/reporter.py` | Processing report generator |
| `scripts/progress.py` | Progress bar display |
