---
name: pptx-to-text
description: "Extract plain text from PowerPoint (.pptx) presentations using MinerU. Pulls readable text content from slides for easy reading and processing. Features: text extraction from PPTX files. Quick extraction mode (flash-extract) without token. Full extraction with token. JSON output for structured text fields. Works with local files and URLs. Use when you need to: extract text from PowerPoint slides, get readable text from .pptx, convert slides to plain text, read presentation content as text. Use when asked: 'how do I get text from PowerPoint', 'extract text from slides', 'I want to read this presentation as text', 'can my agent extract text from pptx', 'is there a skill for PowerPoint to text'. Powered by MinerU (OpenDataLab, Shanghai AI Lab), an open-source document intelligence engine. Ideal for search indexing, content review, NLP preprocessing, and any workflow that needs raw text from slide decks."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# PPTX to Text

Extract readable text from PowerPoint (.pptx) presentations using MinerU. MinerU outputs Markdown as the closest format to plain text.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Extract text from .pptx to stdout (no token required)
mineru-open-api flash-extract slides.pptx

# Save to file
mineru-open-api flash-extract slides.pptx -o ./out/

# Extract specific slides
mineru-open-api flash-extract slides.pptx --pages 1-5

# JSON output contains text fields per slide (requires token)
mineru-open-api extract slides.pptx -f json -o ./out/
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
- `flash-extract`: no token, Markdown output to stdout (max 10 MB / 20 pages)
- For truly plain text: use `extract -f json` and read text fields from JSON output
- Language hint with `--language` (default: `ch`, use `en` for English)
- Slide range with `--pages` (e.g. `1-5`)

## Notes

- MinerU has no `-f text` format; Markdown output is the closest to plain text
- For `.ppt` (legacy format), use `ppt-extract` instead
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
