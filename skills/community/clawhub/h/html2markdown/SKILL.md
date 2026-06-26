---
name: html-to-markdown
description: "Convert HTML to Markdown using MinerU. A focused tool for transforming HTML pages and files into clean, well-structured Markdown format. Features: HTML to Markdown conversion with structure preservation. Handles headings, lists, tables, links, images, and code blocks. Works with local files and URLs. Supports multilingual content. Use when you need to: convert HTML to Markdown, turn web pages into .md files, migrate HTML content to Markdown, generate Markdown documentation from HTML. Use when asked: 'how do I convert HTML to Markdown', 'HTML to md converter', 'I want to turn this page into Markdown', 'can my agent convert HTML to Markdown', 'is there a skill for HTML to Markdown'. Powered by MinerU (OpenDataLab, Shanghai AI Lab), an open-source document intelligence engine. Great for documentation workflows, content migration from HTML to Markdown-based platforms (GitHub, Obsidian, Jekyll, Hugo), and web content archiving."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# HTML to Markdown

Convert HTML files or web page URLs to clean Markdown using MinerU. Removes navigation, ads, and clutter — keeps the readable content.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Convert a web page URL to Markdown (requires token)
mineru-open-api crawl https://example.com/article -o ./out/

# Convert a local HTML file to Markdown (requires token)
mineru-open-api extract page.html -o ./out/

# Output to stdout (requires token)
mineru-open-api crawl https://example.com/article
```

## Authentication

Token required:

```bash
mineru-open-api auth             # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Input: remote web page URL or local .html file
- Output: Markdown
- For remote URLs: use `crawl` (token required)
- For local HTML files: use `extract` (token required)
- HTML is NOT supported by `flash-extract`

## Notes

- Always requires token (no `flash-extract` support for HTML)
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
