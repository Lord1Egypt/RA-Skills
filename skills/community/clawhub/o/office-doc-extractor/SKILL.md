---
name: office-doc-extractor
description: Convert Microsoft Office documents (DOCX, XLSX, PPTX) to Markdown without any external dependencies. Use when the user needs to extract text from Word documents, Excel spreadsheets, or PowerPoint presentations for analysis, indexing, or LLM processing. Pure Python implementation — no pip install, no subprocess calls, no network downloads required. Works offline.
---

# Office Document Extractor

Zero-dependency converter for Microsoft Office documents. Extracts text and structure from DOCX, XLSX, and PPTX files into clean Markdown.

## Quick Start

```bash
# Single file
python3 scripts/main.py report.docx -o report.md

# Batch convert a directory
python3 scripts/main.py ./documents --batch -o ./markdown
```

## Supported Formats

| Format | Extension | Output |
|---|---|---|
| Word | .docx | Headings, paragraphs |
| Excel | .xlsx | Tables (one per sheet) |
| PowerPoint | .pptx | Slides as sections |

## How It Works

- **DOCX**: Parses the ZIP archive's XML directly using Python's `zipfile` and `xml.etree`
- **XLSX**: Uses bundled `openpyxl` (pure Python, no C extensions)
- **PPTX**: Parses the ZIP archive's slide XML directly

No external commands, no network calls, no pip install required.

## Usage

### Single File

```bash
python3 scripts/main.py <input_file> [-o <output.md>]
```

Auto-detects format from file extension. If `-o` is omitted, outputs to `<input>.md`.

### Batch Conversion

```bash
python3 scripts/main.py <input_directory> --batch [-o <output_directory>]
```

Converts all `.docx`, `.xlsx`, `.pptx` files in the directory. Results saved to `markdown_output/` by default.

## Resources

### scripts/

- **main.py** — Unified CLI for single-file and batch conversion
- **docx_extractor.py** — DOCX → Markdown (standard library only)
- **xlsx_extractor.py** — XLSX → Markdown tables (bundled openpyxl)
- **pptx_extractor.py** — PPTX → Markdown (standard library only)

### Bundled Dependencies

- **openpyxl/** — Pure Python Excel library (v3.1.5)
- **et_xmlfile/** — openpyxl dependency (pure Python)

## Limitations

- Does not extract images or embedded objects (text only)
- Does not preserve complex formatting (colors, fonts, layouts)
- Does not handle encrypted/password-protected files
- No OCR for scanned documents (use OpenClaw's native `pdf` tool for that)

## Why This Skill?

Existing markitdown-based skills require `pip install` or external CLI tools, which triggers ClawHub security warnings. This skill is **100% self-contained** — install it and use it immediately, even offline.
