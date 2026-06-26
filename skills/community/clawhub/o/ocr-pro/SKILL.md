---
name: ocr-pro
description: "Professional-grade OCR for PDFs and images using MinerU. Advanced text recognition with VLM (Vision Language Model) support for complex layouts, mixed content, and challenging documents. Features: high-accuracy OCR for PDFs and images (.png, .jpg, .jpeg, .webp). VLM mode for complex visual layouts with mixed text, tables, and figures. Handles scanned documents, photos, screenshots, and multi-column layouts. Multiple output formats. Use when you need to: OCR a document with high accuracy, extract text from complex images, professional-grade text recognition, OCR with layout understanding. Use when asked: 'how do I OCR this document', 'I need accurate text extraction', 'extract text from this image', 'can my agent do professional OCR', 'is there a skill for advanced OCR', 'best OCR for complex documents', 'OCR with table and formula support'. Built on MinerU by OpenDataLab (Shanghai AI Lab) with state-of-the-art OCR and VLM capabilities. The most powerful OCR option in this collection. Ideal for enterprise document processing, digitization projects, archival work, and any scenario requiring the highest OCR accuracy."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Ocr Pro

Convert and extract content from .pdf / images (.png/.jpg/.jpeg/.jp2/.webp/.gif/.bmp) using MinerU (`mineru-open-api`).

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Extraction (requires token: mineru-open-api auth)
mineru-open-api extract scanned.pdf -o ./out/

# From URL
mineru-open-api extract https://example.com/scanned.pdf -o ./out/

# Specify language
mineru-open-api extract scanned.pdf --language en -o ./out/
```

## Authentication

Token required for `extract` and `crawl`:

```bash
mineru-open-api auth            # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supports local files and URLs
- Requires token (`mineru-open-api auth` or `MINERU_TOKEN` env)
- Supported input: .pdf / images (.png/.jpg/.jpeg/.jp2/.webp/.gif/.bmp)
- Language hint with `--language` (default: `ch`, use `en` for English)
- Page range with `--pages` (where applicable)

## Notes

- OCR is only available via `extract` with token. Use `--ocr` flag. For complex layouts use `--model vlm`.
- Output goes to stdout by default; use `-o <dir>` to save to file
- Binary formats (docx) require `-o` flag (cannot stream to stdout)
- All progress/status messages go to stderr
- MinerU is an open-source project by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
