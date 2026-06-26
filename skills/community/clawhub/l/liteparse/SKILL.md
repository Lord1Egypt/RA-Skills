---
name: liteparse
description: Parse, extract text from, and screenshot PDF and document files locally using the LiteParse CLI (`lit`). Use when asked to extract text from a PDF, parse a Word/Excel/PowerPoint file, batch-process a folder of documents, or generate page screenshots for LLM vision workflows. Runs entirely offline — no cloud, no API key. Supports PDF, DOCX, XLSX, PPTX, images (jpg/png/webp), and more. Triggers on phrases like "extract text from this PDF", "parse this document", "get the text out of", "screenshot this PDF page", or any request to read/extract content from a file.
---

# LiteParse

Local document parser built on PDF.js + Tesseract.js. Zero cloud dependencies.

**Binary:** `lit` (installed globally via npm)
**Docs:** https://developers.llamaindex.ai/liteparse/

## Quick Reference

```bash
# Parse a PDF to text (stdout)
lit parse document.pdf

# Parse to file
lit parse document.pdf -o output.txt

# Parse to JSON (includes bounding boxes)
lit parse document.pdf --format json -o output.json

# Specific pages only
lit parse document.pdf --target-pages "1-5,10,15-20"

# No OCR (faster, text-layer PDFs only)
lit parse document.pdf --no-ocr

# Batch parse a directory
lit batch-parse ./input-dir ./output-dir

# Screenshot pages (for vision model input)
lit screenshot document.pdf -o ./screenshots
lit screenshot document.pdf --target-pages "1,3,5" --dpi 300 -o ./screenshots
```

## Output Formats

| Format | Use case |
|--------|----------|
| `text` (default) | Plain text extraction, feeding into prompts |
| `json` | Structured output with bounding boxes, useful for layout-aware tasks |

## OCR Behavior

- OCR is **on by default** via Tesseract.js (downloads ~10MB English data on first run)
- First run will be slow; subsequent runs use cached data
- `--no-ocr` for pure text-layer PDFs (faster, no network needed)
- For multi-language: `--ocr-language fra+eng`

## Supported File Types

Works natively: **PDF**

Requires **LibreOffice** (`brew install --cask libreoffice`): .docx, .doc, .xlsx, .xls, .pptx, .ppt, .odt, .csv

Requires **ImageMagick** (`brew install imagemagick`): .jpg, .png, .gif, .bmp, .tiff, .webp

## Installation Notes

- Installed via npm: `npm install -g @llamaindex/liteparse`
- Brew formula exists (`brew tap run-llama/liteparse`) but requires current macOS CLT — use npm as primary install path on this machine
- Binary path: `/opt/homebrew/bin/lit`

## Workflow Tips

- For **VA forms, job description PDFs, military docs**: `lit parse file.pdf -o /tmp/output.txt` then read into context
- For **scanned PDFs** (no text layer): OCR is required; complex layouts may degrade — consider LlamaParse cloud for critical docs
- For **vision model workflows**: use `lit screenshot` to generate page images, then pass to `image` tool or similar
- For **batch jobs**: use `lit batch-parse` — it reuses the PDF engine across files for efficiency

## Limitations

- Complex tables, multi-column layouts, and scanned government forms may produce imperfect output
- LlamaParse (cloud) handles the hard cases: https://cloud.llamaindex.ai
- Max recommended DPI for screenshots: 300 (higher = slower, larger files)

## Reference

See `references/output-examples.md` for sample JSON/text output structure.
