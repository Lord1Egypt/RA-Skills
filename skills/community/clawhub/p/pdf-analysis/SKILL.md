---
name: pdf-analysis
description: "Analyze the structure, layout, and content of PDF documents using MinerU. Returns structured output preserving headings, tables, images, formulas, and document hierarchy. Features: comprehensive PDF analysis. Detects document structure: headings, paragraphs, tables, images, formulas. Multiple output formats (Markdown, HTML, JSON, LaTeX, DOCX). OCR and VLM modes for scanned or complex PDFs. Page range selection. Use when you need to: analyze a PDF document, understand PDF structure, inspect PDF content and layout, get a detailed breakdown of a PDF. Use when asked: 'how do I analyze this PDF', 'what is inside this PDF', 'I want to understand this PDF structure', 'can my agent analyze PDF files', 'break down this PDF for me', 'inspect this PDF document'. Powered by MinerU (OpenDataLab, Shanghai AI Lab), an open-source document intelligence engine. The most comprehensive PDF analysis tool in this collection. Ideal for researchers, data analysts, document processing pipelines, and anyone who needs deep insight into PDF document structure and content."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# PDF Analysis

Analyze and extract structured content from PDF files using MinerU. Returns Markdown with layout, headings, and structure preserved.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Quick analysis, no token required (max 10 MB / 20 pages)
mineru-open-api flash-extract report.pdf

# Save to directory
mineru-open-api flash-extract report.pdf -o ./out/

# From URL
mineru-open-api flash-extract https://example.com/report.pdf

# With language hint
mineru-open-api flash-extract report.pdf --language en

# Full analysis with tables and formulas (requires token)
mineru-open-api extract report.pdf -o ./out/
```

## Authentication

No token needed for `flash-extract`. Token required for `extract`:

```bash
mineru-open-api auth             # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supported input: .pdf (local file or URL)
- `flash-extract`: quick, no token, max 10 MB / 20 pages, Markdown output only
- `extract`: token required, full features (tables, formulas, OCR, multi-format output)
- Language hint with `--language` (default: `ch`, use `en` for English)
- Page range with `--pages` (e.g. `1-10`)

## Notes

- Use `flash-extract` for quick reads; use `extract` for tables, formulas, or files over 10 MB
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
