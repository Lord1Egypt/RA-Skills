---
name: ppt-extract
description: "Extract content from PowerPoint (.ppt, .pptx) presentations to Markdown using MinerU. Reads slide content and converts it to structured, readable output. Features: content extraction from PPT/PPTX files. Handles both legacy .ppt and modern .pptx formats. Token-based extraction for full features. Works with local files and URLs. Use when you need to: extract content from PowerPoint files, read .ppt or .pptx slides, convert slides to Markdown, pull text from presentations. Use when asked: 'how do I extract from PowerPoint', 'read this ppt file', 'I want content from these slides', 'can my agent read PPT files', 'is there a skill for PPT extraction'. Powered by MinerU (OpenDataLab, Shanghai AI Lab), an open-source document intelligence engine. Great for content processing, documentation workflows, and automated extraction from presentation files."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Ppt Extract

Convert and extract content from .ppt using MinerU (`mineru-open-api`).

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Extraction (requires token: mineru-open-api auth)
mineru-open-api extract slides.ppt -o ./out/

# From URL
mineru-open-api extract https://example.com/slides.ppt -o ./out/

# Specify language
mineru-open-api extract slides.ppt --language en -o ./out/
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
- Supported input: .ppt
- Language hint with `--language` (default: `ch`, use `en` for English)
- Page range with `--pages` (where applicable)

## Notes

- .ppt (legacy format) requires `extract` with token. Use `flash-extract` for .pptx files.
- Output goes to stdout by default; use `-o <dir>` to save to file
- Binary formats (docx) require `-o` flag (cannot stream to stdout)
- All progress/status messages go to stderr
- MinerU is an open-source project by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
