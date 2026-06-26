---
name: html-analysis
description: "Analyze the structure and content of HTML documents using MinerU. Returns structured Markdown with layout information, headings, and content hierarchy preserved. Features: deep HTML content analysis. Preserves structural hierarchy and formatting. Identifies content sections, headings, tables, and lists. Full analysis mode with comprehensive output. Use when you need to: analyze HTML document structure, understand web page content layout, inspect HTML headings and sections, get a structural overview of an HTML file. Use when asked: 'how do I analyze this HTML', 'what is the structure of this web page', 'I want to understand this HTML layout', 'can my agent analyze HTML files', 'break down this HTML for me'. Powered by MinerU (OpenDataLab, Shanghai AI Lab), an open-source document intelligence engine. Ideal for web developers, SEO analysts, content auditors, and anyone who needs to understand HTML document structure."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# HTML Analysis

Analyze and extract structured content from local HTML files using MinerU. Preserves document structure as Markdown. For live web page URLs, use `mineru-open-api crawl`.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Analyze a local HTML file (requires token)
mineru-open-api extract page.html -o ./out/

# Analyze a remote HTML file by URL (requires token)
mineru-open-api extract https://example.com/page.html -o ./out/

# Crawl a live web page (requires token)
mineru-open-api crawl https://example.com/article -o ./out/
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
- HTML input requires `extract` (token required) — not supported by `flash-extract`
- For live web pages (rendered JS content), use `mineru-open-api crawl`
- Language hint with `--language` (default: `ch`, use `en` for English)

## Notes

- HTML is NOT supported by `flash-extract` — use `extract` with token
- For web page crawling, use `mineru-open-api crawl <URL>` instead of `extract`
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
