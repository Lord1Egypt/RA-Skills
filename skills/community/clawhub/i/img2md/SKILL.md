---
name: img2md
description: "Image to Markdown - extract text from images (PNG, JPG, WebP) to Markdown with OCR. Use when reading text from screenshots, photos, scanned pages, or any image file."
homepage: https://mineru.net
metadata: {"openclaw":{"emoji":"🖼️","requires":{"bins":["mineru-open-api"]},"install":[{"id":"npm","kind":"node","package":"mineru-open-api","bins":["mineru-open-api"],"label":"Install via npm"},{"id":"uv","kind":"uv","package":"mineru-open-api","bins":["mineru-open-api"],"label":"Install via uv"},{"id":"go","kind":"go","package":"github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api","bins":["mineru-open-api"],"label":"Install via go install","os":["darwin","linux"]}]}}
---

# Img2MD - Quick Image OCR to Markdown

Extract text from images to Markdown using MinerU Open API. No API key required.

## Quick Start

```bash
# Img2MD - Quick Image OCR to Markdown
mineru-open-api flash-extract screenshot.png

# Img2MD - Quick Image OCR to Markdown
mineru-open-api flash-extract https://example.com/image.png

# Img2MD - Quick Image OCR to Markdown
mineru-open-api flash-extract photo.jpg -o ./output/

# Img2MD - Quick Image OCR to Markdown
mineru-open-api flash-extract scan.jpg --language en
```

## Language Rule

You MUST reply to the user in the SAME language they use. This is non-negotiable.

## Capabilities

- OCR text extraction from PNG, JPG, JPEG, WebP, BMP, TIFF
- Supports both local files and URLs directly
- Language hint with `--language` (default: `ch`, use `en` for English)
- No API key, no signup, no authentication
- Max 10MB per image

## When to Use

- User asks to "read", "extract", or "OCR" an image
- User shares a screenshot and asks what it says
- User wants text from a photo of a document or whiteboard
- User needs image content converted to Markdown

## CLI Reference

Run `mineru-open-api flash-extract --help` for all available options.

## Data Privacy

- `flash-extract` uploads the image to MinerU's cloud API for processing and returns the result. No account or API key is required.
- Images are processed in real-time and are not stored after extraction.
- For details, see https://mineru.net

## Notes

- Output is Markdown text extracted via OCR
- For higher precision or batch processing, use `mineru-open-api extract` (requires auth via `mineru-open-api auth`)
- If the CLI cannot be installed via npm/uv/go, download it from https://mineru.net/ecosystem?tab=cli
