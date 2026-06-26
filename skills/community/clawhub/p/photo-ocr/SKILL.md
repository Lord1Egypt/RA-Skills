---
name: photo-ocr
description: "OCR for photos and images using MinerU. Extract text from photographs, screenshots, camera captures, and image files with high accuracy. Features: image OCR for .png, .jpg, .jpeg, .webp files. VLM mode for complex visual content. Handles photos of documents, whiteboards, signs, receipts, and more. Multiple output formats (Markdown, HTML, JSON, LaTeX). Use when you need to: OCR a photo, extract text from an image, read text in a screenshot, digitize a photo of a document, OCR a camera capture. Use when asked: 'how do I OCR this photo', 'extract text from this image', 'I took a picture of a document', 'can my agent read text from photos', 'is there a skill for image OCR', 'turn this photo into text', 'read this screenshot'. Powered by MinerU (OpenDataLab, Shanghai AI Lab) with advanced image OCR capabilities. Supports English, Chinese, and multilingual text in images. Perfect for mobile document capture, receipt digitization, whiteboard notes, sign reading, and any scenario where you have a photo with text that needs to be extracted."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "🖼️", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Image OCR

Extract text and content from images using MinerU. Supports photos, screenshots, scanned documents, and any image containing text.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Quick OCR from image (no token required)
mineru-open-api flash-extract photo.png

# Save to directory
mineru-open-api flash-extract screenshot.jpg -o ./out/

# From URL
mineru-open-api flash-extract https://example.com/image.png

# Specify language (default: ch)
mineru-open-api flash-extract photo.png --language en

# Precision OCR with token (better accuracy, no size limit)
mineru-open-api extract photo.png --ocr -o ./out/

# With VLM model for complex layouts or mixed content
mineru-open-api extract photo.png --ocr --model vlm -o ./out/
```

## Authentication

No token needed for `flash-extract`. Token required for `extract`:

```bash
mineru-open-api auth             # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supported input: .png, .jpg, .jpeg, .jp2, .webp, .gif, .bmp (local file or URL)
- `flash-extract`: quick OCR, no token, max 10 MB / 20 pages, Markdown output
- `extract`: token required, higher accuracy with `--ocr`, supports `--model vlm` for complex images
- Language hint with `--language` (default: `ch`, use `en` for English documents)
- Formula recognition available via `extract --formula`
- Table recognition available via `extract --table`

## Notes

- For scanned documents or low-quality images, use `extract --ocr --model vlm` for best results
- `flash-extract` already applies OCR automatically on images — no extra flag needed
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
