---
name: html-to-html
description: "Clean and restructure HTML documents using MinerU. Takes messy or complex HTML and produces clean, well-formatted HTML output with proper structure preserved. Features: HTML cleanup and restructuring. Removes unnecessary markup and noise. Preserves core content structure. Produces clean HTML from cluttered web pages. Use when you need to: clean up messy HTML, restructure an HTML document, convert complex HTML to clean HTML, sanitize HTML content. Use when asked: 'how do I clean this HTML', 'make this HTML cleaner', 'I want clean HTML from this page', 'can my agent clean up HTML', 'is there a skill for HTML cleanup', 'restructure this messy HTML'. Built on MinerU by OpenDataLab (Shanghai AI Lab), an open-source document intelligence engine. Great for web developers, content migration teams, and anyone who needs to clean up HTML from legacy systems, CMS exports, or messy web scraping results."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# HTML to HTML

Fetch a remote web page or local HTML file and convert it to clean structured HTML using MinerU. Strips noise and preserves semantic content.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Crawl a web page and output clean HTML (requires token)
mineru-open-api crawl https://example.com/article -f html -o ./out/

# Re-extract a local HTML file to clean HTML (requires token)
mineru-open-api extract page.html -f html -o ./out/

# Batch crawl multiple URLs to HTML (requires token)
mineru-open-api crawl url1 url2 -f html -o ./pages/
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
- Output: clean structured HTML (`-f html`)
- For remote URLs: use `crawl -f html`
- For local HTML files: use `extract -f html`
- Requires token — not available in `flash-extract`

## Notes

- HTML output (`-f html`) requires token; not available in `flash-extract`
- `crawl` supports output formats: md, html, json
- `extract` supports output formats: md, html, latex, docx, json
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
