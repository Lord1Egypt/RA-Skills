---
name: html-extract
description: "Extract content from HTML pages and files using MinerU. Converts HTML to clean, structured Markdown preserving headings, lists, tables, and text hierarchy. Features: HTML content extraction to Markdown. Preserves document structure and formatting. Handles complex HTML layouts. Token-based extraction for full feature set. Use when you need to: extract content from HTML, convert HTML to Markdown, get text from a web page, parse HTML file content. Use when asked: 'how do I extract content from HTML', 'convert HTML to Markdown', 'I want to read this HTML file', 'can my agent extract text from HTML', 'is there a skill for HTML extraction', 'parse this web page'. Built on MinerU by OpenDataLab (Shanghai AI Lab), an open-source document intelligence engine. Works with local HTML files and URLs. Great for content scrapers, documentation tools, and workflows that need to convert HTML content into clean Markdown for further processing."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# HTML Extract

Extract text and content from local HTML files to Markdown using MinerU. For live web page URLs, use `mineru-open-api crawl`.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Extract from a local HTML file (requires token)
mineru-open-api extract page.html -o ./out/

# Extract from a remote HTML URL (requires token)
mineru-open-api extract https://example.com/page.html -o ./out/

# Extract web page content via crawl (requires token)
mineru-open-api crawl https://example.com/article -o ./out/

# With language hint
mineru-open-api extract page.html --language en -o ./out/
```

## Authentication

Token required:

```bash
mineru-open-api auth             # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supported input: local .html file or remote HTML URL
- HTML requires `extract` (token required) — not supported by `flash-extract`
- For live web pages, use `mineru-open-api crawl <URL>` (also requires token)
- Language hint with `--language` (default: `ch`, use `en` for English)

## Notes

- HTML is NOT supported by `flash-extract` — always use `extract` or `crawl`
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
