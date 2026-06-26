---
name: pixmind-image-compress
description: "Cloud-powered image compression and resize — compress JPG/PNG/WebP/HEIC to WebP/AVIF, resize images, batch process folders. No local dependencies, uses Tencent Cloud COS imageMogr2 via Pixmind API. Save 60-90% file size with scene presets (web, wechat, email, thumbnail). Supports format conversion, quality control, and dimension adjustment."
homepage: https://www.pixmind.io
metadata: {"openclaw": {"requires": {"env": ["PIXMIND_API_KEY"]}, "primaryEnv": "PIXMIND_API_KEY"}}
---

# Pixmind Image Compress

Cloud-powered image compression and resize. Compress JPG, PNG, WebP, HEIC photos to WebP, AVIF or smaller JPG — save 60-90% file size with zero local dependencies.

Powered by [Pixmind](https://www.pixmind.io) + Tencent Cloud COS [imageMogr2](https://cloud.tencent.com/document/product/460/36540).

## Why this skill?

- **Zero install** — No sharp, ImageMagick, or native modules. Runs on any platform with just an API key.
- **Cloud-processed** — Handles HEIC, AVIF, TPG formats that local tools struggle with.
- **Scene presets** — One command for web, WeChat, email, or archival use.
- **Batch ready** — Compress entire folders recursively.
- **Safe by default** — Never overwrites originals, auto-numbered output.

## When to use

**Use this skill when the user mentions:**

1. **Compress** — "图片太大"、"压缩一下"、"缩小文件"、"reduce image size"、"compress photo"、"file too large"
2. **Format conversion** — "转成 JPG"、"PNG 转 WebP"、"HEIC 转 JPG"、"convert to webp"、"change format"
3. **Resize** — "缩小到 1920px"、"调整尺寸"、"resize image"、"reduce dimensions"、"scale down"
4. **Batch** — "批量压缩"、"处理这个文件夹"、"compress all images"、"batch resize"
5. **Scene optimization** — "用于邮件附件"、"上传网站"、"微信发送"、"optimize for web"、"shrink for email"
6. **Typical triggers**:
   - "帮我压缩这张图片，文件太大了发不了微信"
   - "Screenshot.png is 10MB, make it smaller"
   - "Convert all PNGs in this folder to WebP"
   - "Resize these photos to max 1920px width"

**Do NOT trigger for:**
- Image generation (use `pixmind-image` skill)
- Image editing (crop, rotate, watermark, filters)
- Image analysis (OCR, content recognition, EXIF reading)

## Prerequisites

1. Register at [pixmind.io](https://www.pixmind.io/) — **200 bonus points on signup** (free trial)
2. Create an API key at [pixmind.io/api-keys](https://www.pixmind.io/api-keys)
3. Set env `PIXMIND_API_KEY` with your key

## Quick Start

```bash
# Compress a single image (local file)
node {baseDir}/compress.js --file ~/Desktop/photo.png --preset web

# Compress from URL
node {baseDir}/compress.js --url https://example.com/image.jpg --quality 80 --format webp

# Resize to max 1920px width
node {baseDir}/compress.js --file photo.jpg --width 1920

# Batch compress a folder
node {baseDir}/compress.js --dir ~/Pictures/ --preset web --recursive
```

## Presets

Quick scene-based compression — no need to remember quality numbers:

| Preset | Quality | Format | Use Case | Savings |
|--------|---------|--------|----------|---------|
| `web` | 75 | WebP | Website, blog, CMS upload | 60-70% |
| `wechat` | 65 | JPG | WeChat, social media sharing | 70-80% |
| `email` | 55 | JPG | Email attachments, fast transfer | 80-90% |
| `quality` | 95 | original | High-quality archiving, print | 30-40% |
| `thumbnail` | 60 | WebP | Thumbnails, previews, avatars | 80-90% |

## API Details

**Endpoint**: `POST https://aihub-admin.aimix.pro/open/cos/image/compress`
**Auth**: Header `X-API-Key: {API_KEY}` and `X-App-Key: {APP_KEY}`

### Request Body (JSON)

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `imageUrl` | One of | string | Image URL (COS or external link) |
| `imageBase64` | One of | string | Base64 image data (supports `data:image/xxx;base64,` prefix) |
| `format` | No | string | Output format: `webp`, `jpg`, `png`, `avif`, `heif`, `tpg` |
| `quality` | No | number | Compression quality 1-100 (default: 75) |
| `width` | No | number | Target width in pixels (maintains aspect ratio) |
| `height` | No | number | Target height in pixels (maintains aspect ratio) |
| `mode` | No | string | Response type: `url` (default) or `base64` |

### Response Format

```json
{
  "code": 1000,
  "message": "success",
  "data": {
    "originalUrl": "https://bucket.cos.region.myqcloud.com/image.jpg",
    "compressedUrl": "https://bucket.cos.region.myqcloud.com/image.jpg?imageMogr2/format/webp/quality/75",
    "originalSize": 1024000,
    "compressedSize": 256000,
    "format": "webp",
    "quality": 75,
    "width": 800,
    "height": 600
  }
}
```

## Supported Formats

**Input**: JPG, JPEG, PNG, WebP, GIF, BMP, HEIC, HEIF
**Output**: `webp`, `jpg`, `png`, `avif`, `heif`, `tpg`

## CLI Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--url` | `-u` | string | — | Image URL to compress |
| `--file` | `-f` | string | — | Local image file path |
| `--dir` | `-d` | string | — | Directory for batch processing |
| `--format` | | string | original | Output: webp, jpg, png, avif, heif, tpg |
| `--quality` | `-q` | number | 75 | Quality 1-100 |
| `--width` | `-w` | number | — | Target width (maintain ratio) |
| `--height` | | number | — | Target height (maintain ratio) |
| `--preset` | `-p` | string | — | web, wechat, email, quality, thumbnail |
| `--output` | `-o` | string | auto | Output directory |
| `--recursive` | `-r` | boolean | false | Process subdirectories |
| `--mode` | | string | url | Response: url or base64 |

## Output Rules

- Compressed files saved to `~/Downloads/compressed-images/{date}/` by default
- Original files are **never** modified or overwritten
- Duplicate filenames auto-numbered: `photo_001.jpg`, `photo_002.jpg`
- Batch mode preserves original directory structure

## Guidelines

1. For local files, the script auto-reads and converts to Base64 for upload
2. Default to quality 75 — good balance of quality and size
3. Match presets to use cases: `web` for sites, `wechat` for sharing, `email` for attachments
4. When resizing, specify only one dimension to maintain aspect ratio
5. For batch processing, show progress and total savings summary
6. After compression, always show before/after size and savings percentage
7. Prefer `webp` for web — best compression with good quality
8. For photos: recommend `jpg` or `webp`; for screenshots/diagrams: `png` or `webp`
9. HEIC (iPhone) photos are natively supported — no extra dependencies needed
