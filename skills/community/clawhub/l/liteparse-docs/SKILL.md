---
name: liteparse
version: 1.0.0
description: Use when parsing PDFs, DOCX, PPTX, XLSX, or images locally. Supports text extraction, JSON output with bounding boxes, batch processing, and page screenshots. No cloud dependencies.
license: Apache-2.0
---

# LiteParse

Parse unstructured documents (PDF, DOCX, PPTX, XLSX, images, and more) locally with LiteParse: fast, lightweight, no cloud dependencies or LLM required.

## Installation

Already installed via Homebrew:
```bash
brew install llamaindex-liteparse
```

Verify:
```bash
lit --version
```

## Supported Formats

| Category | Formats |
|----------|---------|
| PDF | `.pdf` |
| Word | `.doc`, `.docx`, `.docm`, `.odt`, `.rtf` |
| PowerPoint | `.ppt`, `.pptx`, `.pptm`, `.odp` |
| Spreadsheets | `.xls`, `.xlsx`, `.xlsm`, `.ods`, `.csv`, `.tsv` |
| Images | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.svg` |

**Dependencies:**
- Office documents → LibreOffice (`brew install --cask libreoffice`)
- Images → ImageMagick (`brew install imagemagick`)

## Usage

### Parse a Single File

```bash
# Basic text extraction
lit parse document.pdf

# JSON output with bounding boxes
lit parse document.pdf --format json -o output.json

# Specific page range
lit parse document.pdf --target-pages "1-5,10,15-20"

# Disable OCR (faster, text-only PDFs)
lit parse document.pdf --no-ocr

# Higher DPI for better quality
lit parse document.pdf --dpi 300
```

### Batch Parse a Directory

```bash
lit batch-parse ./input-directory ./output-directory

# Only PDFs, recursively
lit batch-parse ./input ./output --extension .pdf --recursive
```

### Generate Page Screenshots

```bash
# All pages
lit screenshot document.pdf -o ./screenshots

# Specific pages
lit screenshot document.pdf --target-pages "1,3,5" -o ./screenshots

# High-DPI PNG
lit screenshot document.pdf --dpi 300 --format png -o ./screenshots
```

## Key Options

| Option | Description |
|--------|-------------|
| `--format json` | Structured JSON with bounding boxes |
| `--format text` | Plain text (default) |
| `--target-pages "1-5,10"` | Parse specific pages |
| `--dpi 300` | Higher rendering quality |
| `--no-ocr` | Disable OCR (faster for text PDFs) |
| `--ocr-language fra` | Set OCR language |
| `-o output.json` | Save to file |

## Config File

For repeated use, create `liteparse.config.json`:

```json
{
  "ocrLanguage": "en",
  "ocrEnabled": true,
  "maxPages": 1000,
  "dpi": 150,
  "outputFormat": "json",
  "preciseBoundingBox": true
}
```

Use with:
```bash
lit parse document.pdf --config liteparse.config.json
```

## When to Use

- **PDF text extraction** — fast local parsing
- **Document conversion** — Office docs to text/JSON
- **Screenshot generation** — for LLM visual analysis
- **Batch processing** — multiple files at once
- **Offline/air-gapped** — no cloud required