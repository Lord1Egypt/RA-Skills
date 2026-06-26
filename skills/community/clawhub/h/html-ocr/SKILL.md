---
name: html-ocr
description: "OCR for HTML pages containing image-embedded or scanned content. Uses MinerU to extract text from images within HTML files and web pages. Features: OCR extraction for image content in HTML files. VLM mode for complex mixed-content pages. Handles HTML with embedded scanned images. Converts image text to searchable Markdown. Use when you need to: OCR images in HTML pages, extract text from image-heavy web pages, read scanned content embedded in HTML. Use when asked: 'how do I OCR an HTML page', 'extract text from images in HTML', 'this web page has images instead of text', 'can my agent OCR HTML content', 'is there a skill for HTML OCR'. Built on MinerU by OpenDataLab (Shanghai AI Lab) with advanced OCR capabilities. Perfect for web archiving, accessibility improvements, and content extraction from image-heavy web pages."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# HTML OCR

Use OCR to extract text from HTML files that contain scanned images or image-embedded content using MinerU.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# OCR extraction from local HTML file (requires token)
mineru-open-api extract page.html --ocr -o ./out/

# With VLM model for better accuracy
mineru-open-api extract page.html --ocr --model vlm -o ./out/
```

## Authentication

Token required:

```bash
mineru-open-api auth             # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supported input: local .html file
- OCR requires `extract` with token — not available in `flash-extract`
- Use `--ocr` flag to enable OCR on image-embedded content in HTML
- Use `--model vlm` for complex or mixed-content pages

## Notes

- HTML is NOT supported by `flash-extract`; use `extract` with token
- If the HTML has normal text content, OCR is not needed — use `html-extract` instead
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
