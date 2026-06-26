---
name: pdf-to-html
description: "Convert PDF documents to HTML using MinerU. Transforms PDF files into web-ready HTML with structure and formatting preserved. Features: PDF to HTML conversion with layout preservation. Handles text, tables, images, and formatting. Supports local files and URLs. Token-based extraction for full features. Use when you need to: convert a PDF to HTML, turn a PDF into a web page, generate HTML from a PDF document, publish PDF content on the web. Use when asked: 'how do I convert PDF to HTML', 'turn this PDF into HTML', 'I want to view this PDF as a web page', 'can my agent convert PDF to HTML', 'is there a skill for PDF to HTML conversion'. Built on MinerU by OpenDataLab (Shanghai AI Lab), an open-source document intelligence engine. Perfect for web publishers, content teams, and developers who need to convert PDF documents into HTML for web display, CMS integration, or online archives."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# PDF to HTML

Convert PDF files to HTML using MinerU.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Convert PDF to HTML (requires token)
mineru-open-api extract report.pdf -f html -o ./out/

# From URL
mineru-open-api extract https://example.com/report.pdf -f html -o ./out/

# With language hint
mineru-open-api extract report.pdf -f html --language en -o ./out/
```

## Authentication

Token required:

```bash
mineru-open-api auth             # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supported input: .pdf (local file or URL)
- Output format: HTML (`-f html`)
- HTML output requires `extract` with token — not available in `flash-extract`
- Language hint with `--language` (default: `ch`, use `en` for English)
- Page range with `--pages` (e.g. `1-10`)

## Notes

- HTML output (`-f html`) is only available via `extract` with token
- Output goes to stdout by default; use `-o <dir>` to save to a file
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
