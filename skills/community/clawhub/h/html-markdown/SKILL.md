---
name: html-markdown
description: "Convert HTML to Markdown using MinerU's document processing engine. Transforms HTML pages and files into clean, readable Markdown format. Features: HTML to Markdown conversion preserving structure. Handles headings, lists, tables, links, and code blocks. Works with local files and URLs. Clean output suitable for documentation and content systems. Use when you need to: convert HTML to Markdown, transform a web page to .md format, migrate HTML content to Markdown-based systems, generate Markdown from HTML. Use when asked: 'how do I convert HTML to Markdown', 'turn this web page into Markdown', 'I want Markdown from this HTML', 'can my agent convert HTML to md', 'is there a skill for HTML to Markdown conversion'. Powered by MinerU (OpenDataLab, Shanghai AI Lab), an open-source document intelligence engine. Supports multilingual content. Perfect for developers, technical writers, and content teams migrating from HTML-based systems to Markdown workflows (GitHub, Obsidian, Notion, static site generators)."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# HTML Markdown

Convert HTML files to clean Markdown using MinerU. For local HTML files use `extract`; for live web pages use `crawl`.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Convert local HTML file to Markdown (requires token)
mineru-open-api extract page.html -o ./out/

# Convert remote HTML file to Markdown (requires token)
mineru-open-api extract https://example.com/doc.html -o ./out/

# Convert live web page to Markdown via crawl (requires token)
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

- Supported input: local .html file or HTTP/HTTPS URL
- Local `.html` file: use `extract` (token required)
- Live web page URL: use `crawl` (token required)
- HTML is NOT supported by `flash-extract`
- Language hint with `--language` (default: `ch`, use `en` for English)

## Notes

- HTML input always requires token (no `flash-extract` support)
- For live web pages with JavaScript rendering, prefer `crawl`
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
