---
name: pptx-to-html
description: "Convert PowerPoint (.pptx) presentations to HTML using MinerU. Transforms slides into web-ready HTML format with content and structure preserved. Features: PPTX to HTML conversion. Preserves slide content, text, and basic structure. Token-based extraction. Works with local files and URLs. Use when you need to: convert PowerPoint to HTML, turn a .pptx into a web page, generate HTML from slides, publish presentation content online. Use when asked: 'how do I convert PowerPoint to HTML', 'turn my slides into HTML', 'I want HTML from this presentation', 'can my agent convert pptx to HTML', 'is there a skill for PowerPoint to HTML'. Built on MinerU by OpenDataLab (Shanghai AI Lab), an open-source document intelligence engine. Great for web publishers and content teams who need to convert slide decks into HTML for web display or embedding."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Pptx To Html

Convert and extract content from .pptx using MinerU (`mineru-open-api`).

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Convert to HTML (requires token)
mineru-open-api extract slides.pptx -f html -o ./out/

# From URL
mineru-open-api extract https://example.com/slides.pptx -f html -o ./out/
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

- HTML output requires `extract` with token.
- Output goes to stdout by default; use `-o <dir>` to save to file
- Binary formats (docx) require `-o` flag (cannot stream to stdout)
- All progress/status messages go to stderr
- MinerU is an open-source project by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
