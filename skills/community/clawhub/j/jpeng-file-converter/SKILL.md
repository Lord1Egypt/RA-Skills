---
name: jpeng-file-converter
description: "File format conversion skill. Convert between PDF, DOCX, Markdown, HTML, images, audio, and video formats."
version: "1.0.0"
author: "jpeng"
tags: ["file", "convert", "pdf", "docx", "markdown", "image", "audio", "video"]
---

# File Converter

Convert files between different formats.

## When to Use

- User wants to convert a file to another format
- Convert documents (PDF, DOCX, Markdown)
- Convert images (PNG, JPG, WebP, SVG)
- Convert audio/video formats

## Supported Conversions

### Documents
- PDF ↔ DOCX
- Markdown ↔ HTML ↔ PDF
- TXT ↔ DOCX

### Images
- PNG ↔ JPG ↔ WebP ↔ GIF
- SVG → PNG/JPG
- HEIC → JPG/PNG

### Audio
- MP3 ↔ WAV ↔ FLAC ↔ AAC
- M4A ↔ MP3

### Video
- MP4 ↔ WebM ↔ AVI
- Video → GIF

## Usage

### Convert document

```bash
python3 scripts/convert.py \
  --input ./document.docx \
  --output ./document.pdf
```

### Convert image

```bash
python3 scripts/convert.py \
  --input ./image.png \
  --output ./image.jpg \
  --quality 90
```

### Batch convert

```bash
python3 scripts/convert.py \
  --input-dir ./images/ \
  --output-dir ./converted/ \
  --from png \
  --to webp
```

### Resize image

```bash
python3 scripts/convert.py \
  --input ./photo.jpg \
  --output ./thumbnail.jpg \
  --resize 800x600
```

### Extract audio from video

```bash
python3 scripts/convert.py \
  --input ./video.mp4 \
  --output ./audio.mp3 \
  --extract-audio
```

## Output

```json
{
  "success": true,
  "input": "./document.docx",
  "output": "./document.pdf",
  "input_size_kb": 45,
  "output_size_kb": 52
}
```
