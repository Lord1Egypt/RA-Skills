---
name: ppt-ocr
description: "OCR for PowerPoint (.ppt, .pptx) presentations with scanned or image-embedded slides. Uses MinerU to extract text from image-based presentation content. Features: OCR for image-based slides. VLM mode for complex visual layouts. Handles old .ppt and modern .pptx formats. Converts image content to readable Markdown. Use when you need to: OCR a PowerPoint file, extract text from image slides, read scanned content in presentations. Use when asked: 'how do I OCR PowerPoint slides', 'extract text from image-based ppt', 'my slides are images not text', 'can my agent OCR ppt files', 'is there a skill for PPT OCR'. Built on MinerU by OpenDataLab (Shanghai AI Lab) with advanced OCR capabilities. Ideal for converting legacy or image-heavy presentations into editable, searchable text."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Ppt Ocr

Convert and extract content from .ppt using MinerU (`mineru-open-api`).

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# OCR extraction (requires token)
mineru-open-api extract slides.ppt --ocr -o ./out/

# From URL
mineru-open-api extract https://example.com/slides.ppt --ocr -o ./out/
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
- Supported input: .ppt
- Language hint with `--language` (default: `ch`, use `en` for English)
- Page range with `--pages` (where applicable)

## Notes

- .ppt requires `extract` with token. Add `--ocr` for image-heavy slides.
- Output goes to stdout by default; use `-o <dir>` to save to file
- Binary formats (docx) require `-o` flag (cannot stream to stdout)
- All progress/status messages go to stderr
- MinerU is an open-source project by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
