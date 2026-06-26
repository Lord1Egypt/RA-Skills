---
name: pptx-ocr
description: "OCR for PowerPoint (.pptx) presentations with scanned or image-embedded slide content. Uses MinerU to extract text from image-based slides. Features: OCR extraction for image-based PPTX slides. VLM mode for complex visual content. Handles presentations with screenshots, scanned pages, or image-only slides. Converts image content to searchable text. Use when you need to: OCR a PowerPoint presentation, extract text from image-based slides, read scanned content in .pptx. Use when asked: 'how do I OCR PowerPoint slides', 'extract text from image slides', 'my presentation has images instead of text', 'can my agent OCR pptx files', 'is there a skill for PowerPoint OCR'. Built on MinerU by OpenDataLab (Shanghai AI Lab) with advanced OCR capabilities. Perfect for converting image-heavy presentations into searchable, editable text content."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Pptx Ocr

Convert and extract content from .pptx using MinerU (`mineru-open-api`).

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# OCR extraction (requires token)
mineru-open-api extract slides.pptx --ocr -o ./out/

# From URL
mineru-open-api extract https://example.com/slides.pptx --ocr -o ./out/
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
- Supported input: .pptx
- Language hint with `--language` (default: `ch`, use `en` for English)
- Page range with `--pages` (where applicable)

## Notes

- OCR requires `extract` with token. Add `--ocr` flag for image-heavy slides.
- Output goes to stdout by default; use `-o <dir>` to save to file
- Binary formats (docx) require `-o` flag (cannot stream to stdout)
- All progress/status messages go to stderr
- MinerU is an open-source project by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
