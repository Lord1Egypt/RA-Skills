---
name: html-to-text
description: "Convert HTML to plain readable text using MinerU. Strips HTML markup and extracts clean text content from web pages and HTML files. Features: HTML to text conversion. Removes all markup while preserving readable structure. Outputs Markdown as the closest plain-text format. JSON output mode for pure text fields. Works with local files and URLs. Use when you need to: convert HTML to plain text, strip markup from a web page, extract readable text from HTML, get text content from an HTML file. Use when asked: 'how do I get text from HTML', 'strip HTML tags', 'I want plain text from this web page', 'can my agent extract text from HTML', 'is there a skill for HTML to text conversion'. Built on MinerU by OpenDataLab (Shanghai AI Lab), an open-source document intelligence engine. Ideal for search indexing, NLP pipelines, text analysis, and any workflow that needs clean text from HTML sources."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# HTML to Text

Extract plain readable text from HTML files or web pages using MinerU. MinerU outputs Markdown as the closest format to plain text.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Extract text from a local HTML file (requires token)
mineru-open-api extract page.html -o ./out/

# Extract text from a web page (requires token)
mineru-open-api crawl https://example.com/article

# JSON output contains text fields (requires token)
mineru-open-api extract page.html -f json -o ./out/
```

## Authentication

Token required:

```bash
mineru-open-api auth             # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supported input: local .html file or web page URL
- HTML requires `extract` or `crawl` (token required) — not supported by `flash-extract`
- MinerU does not have a `-f text` option; Markdown is the closest plain-text output
- For truly plain text: use `extract -f json` and read the text fields from JSON output
- Language hint with `--language` (default: `ch`, use `en` for English)

## Notes

- MinerU has no `-f text` format; use Markdown output or `-f json` for text fields
- HTML is NOT supported by `flash-extract`
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
