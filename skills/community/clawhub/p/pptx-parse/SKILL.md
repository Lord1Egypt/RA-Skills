---
name: pptx-parse
description: "Parse PowerPoint (.pptx) presentations into structured Markdown using MinerU. Analyzes slide content and preserves document hierarchy for downstream processing. Features: structural parsing of PPTX files. Preserves slide organization and content hierarchy. Quick parse (flash-extract) without token. Full parsing with token. Works with local files and URLs. Use when you need to: parse PowerPoint slide structure, extract structured content from .pptx, analyze presentation layout, get organized output from slides. Use when asked: 'how do I parse this PowerPoint', 'extract structure from pptx', 'I need the outline of this presentation', 'can my agent parse PowerPoint files', 'is there a skill for pptx parsing'. Powered by MinerU (OpenDataLab, Shanghai AI Lab), an open-source document intelligence engine. Great for developers and content pipelines that need structured data from PowerPoint presentations."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# PPTX Parse

Parse PowerPoint (.pptx) presentations into structured Markdown using MinerU. Preserves slide structure and text hierarchy.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Quick parse, no token required
mineru-open-api flash-extract slides.pptx

# Save to directory
mineru-open-api flash-extract slides.pptx -o ./out/

# Parse specific page range
mineru-open-api flash-extract slides.pptx --pages 1-10

# Full parse with token (tables, formulas)
mineru-open-api extract slides.pptx -o ./out/
```

## Authentication

No token needed for `flash-extract`. Token required for `extract`:

```bash
mineru-open-api auth             # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supported input: .pptx (local file or URL)
- `flash-extract`: quick, no token, max 10 MB / 20 pages, Markdown output
- `extract`: token required, full structured parsing with tables and formulas
- Language hint with `--language` (default: `ch`, use `en` for English)
- Slide range with `--pages` (e.g. `1-10`)

## Notes

- For `.ppt` (legacy format), use `ppt-extract` instead
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
