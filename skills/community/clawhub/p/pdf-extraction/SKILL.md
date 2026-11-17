---
name: pdf-extraction
description: "Extract text, tables, and metadata from PDFs. Auto-detects native text vs scanned image pages and routes to pdfplumber or Tesseract OCR."
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires":
          {
            "bins": ["pdf-extract", "tesseract"],
          },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": ".",
              "bins": ["pdf-extract"],
              "label": "Install pdf-extract CLI (pip install -e .)",
            },
          ],
      },
  }
---

# PDF Extraction (auto text / OCR)

Extract content from PDFs without deciding whether each page is selectable text or a scan.

| Page type | Tool |
|-----------|------|
| Native text | `pdfplumber` (text + tables) |
| Scanned / image | PyMuPDF + Tesseract OCR |

## Install

```bash
# System OCR engine (required for scanned pages)
# Ubuntu/Debian:
sudo apt install tesseract-ocr tesseract-ocr-eng
# Optional Traditional Chinese:
# sudo apt install tesseract-ocr-chi-tra

# CLI — from GitHub (recommended)
pip install "git+https://github.com/alex-ht/pdf-extraction.git@v1.0.0"

# Or install from this skill folder after ClawHub install:
# pip install -e .
```

Source: https://github.com/alex-ht/pdf-extraction
## Quick start

```bash
# Auto-detect text vs OCR per page → print text
pdf-extract document.pdf

# Write to file
pdf-extract document.pdf -o out.txt

# See which mode each page will use
pdf-extract document.pdf --analyze-only

# Tables + Markdown
pdf-extract document.pdf --tables --format markdown -o out.md

# JSON (includes per-page mode)
pdf-extract document.pdf --format json -o out.json

# Force mode
pdf-extract scan.pdf --mode ocr --ocr-lang eng
pdf-extract text.pdf --mode text

# Page range
pdf-extract doc.pdf --pages 1-3,5

# Also: python -m pdf_extract document.pdf
```

## Auto mode rules

For each page (`--mode auto`, default):

1. Try native text via pdfplumber; count chars and embedded images
2. Enough text → **text**
3. Sparse text (default &lt; 40 non-whitespace chars) or image-heavy → **ocr**

Tune with `--min-text-chars`. Override with `--mode text` or `--mode ocr`.

## Agent usage

When the user provides a PDF and wants content extracted:

1. Prefer `pdf-extract <file>` (auto mode). Do not ask whether it is text or scanned.
2. Use `--analyze-only` if you only need routing diagnostics.
3. Use `--tables` when tables matter (works best on native-text pages).
4. For Chinese scans, set `--ocr-lang eng+chi_tra` if `chi_tra` is installed.
5. Surface stderr summary lines (which pages used text vs ocr) when useful.

## CLI reference

| Flag | Meaning |
|------|---------|
| `-o`, `--output` | Write to file (default stdout) |
| `-f`, `--format` | `text` \| `json` \| `markdown` |
| `--mode` | `auto` \| `text` \| `ocr` |
| `--pages` | e.g. `1-3,5` |
| `--tables` | Extract tables on text pages |
| `--layout` | Preserve native text layout |
| `--meta` | Include PDF metadata |
| `--ocr-lang` | Tesseract langs (default `eng`) |
| `--ocr-dpi` | OCR render DPI (default `200`) |
| `--analyze-only` | Classification JSON only |
| `-q`, `--quiet` | Suppress progress on stderr |

## Dependencies

- Python 3.10+: `pdfplumber`, `pymupdf`, `Pillow` (see `pyproject.toml`)
- System: `tesseract` (and language packs as needed)
