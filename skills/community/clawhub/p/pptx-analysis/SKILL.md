---
name: pptx-analysis
description: "Analyze the structure and content of PowerPoint (.pptx) presentations using MinerU. Returns structured Markdown with slide content, headings, and layout preserved. Features: structural analysis of PPTX files. Quick analysis (flash-extract) without token. Full analysis with token for detailed inspection. Identifies slide structure, text blocks, and content hierarchy. Use when you need to: analyze a PowerPoint presentation, understand slide structure, inspect .pptx content and layout, get an overview of a presentation. Use when asked: 'how do I analyze this PowerPoint', 'what is inside this pptx', 'I want to understand these slides', 'can my agent analyze PowerPoint files', 'break down this presentation for me'. Built on MinerU by OpenDataLab (Shanghai AI Lab), an open-source document intelligence engine. Ideal for content reviewers, presentation auditors, and automated quality checks on slide decks."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# PPTX Analysis

Analyze and extract structured content from PowerPoint (.pptx) presentations using MinerU. Returns Markdown with slide content and layout preserved.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Quick analysis, no token required
mineru-open-api flash-extract slides.pptx

# Save to directory
mineru-open-api flash-extract slides.pptx -o ./out/

# Full analysis with token (tables, formulas, multi-format)
mineru-open-api extract slides.pptx -o ./out/

# With language hint
mineru-open-api flash-extract slides.pptx --language en
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
- `flash-extract`: quick, no token, max 10 MB / 20 pages, Markdown output only
- `extract`: token required, full features (tables, formulas, multi-format output)
- Language hint with `--language` (default: `ch`, use `en` for English)

## Notes

- For `.ppt` (legacy format), use `ppt-extract` skill instead
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
