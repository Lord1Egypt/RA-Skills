---
name: pdf-to-long-image
description: |
  Convert multi-page PDFs into a single vertical long image by concatenating all pages.
  Use when the user asks to convert PDF to long image, combine PDF pages into one image,
  or create a scrolling screenshot from a PDF document.
---

# PDF to Long Image

Convert multi-page PDFs into a single vertical long image, useful for sharing documents
as scrolling images or creating visual summaries.

## Quick Start

```bash
# Basic usage
uv run python ~/.openclaw/skills/pdf-to-long-image/scripts/pdf_to_long_image.py input.pdf

# Specify output path
uv run python ~/.openclaw/skills/pdf-to-long-image/scripts/pdf_to_long_image.py input.pdf output.png

# Higher resolution
uv run python ~/.openclaw/skills/pdf-to-long-image/scripts/pdf_to_long_image.py input.pdf output.png --scale 3
```

## How It Works

1. Opens the PDF using pymupdf (fitz)
2. Renders each page at the specified scale (default 2x for clarity)
3. Vertically concatenates all pages into a single image
4. Saves as optimized PNG

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `input` | (required) | Path to the PDF file |
| `output` | `input_long.png` | Output image path |
| `--scale` | 2.0 | Render scale factor (higher = more detail) |

## Dependencies

The script requires these packages (install with uv):

```bash
uv pip install pymupdf pillow
```

## Example Output

```
Converting 32 pages from document.pdf...
  Page 1/32: 1684x1190
  Page 2/32: 1684x1190
  ...
Done! Saved to: document_long.png
  Dimensions: 1684x38112 pixels
  File size: 11.23 MB
```

## Script Location

```
~/.openclaw/skills/pdf-to-long-image/scripts/pdf_to_long_image.py
```