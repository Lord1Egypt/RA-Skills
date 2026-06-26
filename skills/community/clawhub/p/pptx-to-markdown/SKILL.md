---
name: pptx-to-markdown
description: "Document to Markdown converter - convert DOCX, PPTX, Excel files to Markdown. Use when extracting content from Word documents, PowerPoint presentations, or Excel spreadsheets."
homepage: https://mineru.net
metadata: {"openclaw":{"emoji":"📑","requires":{"bins":["mineru-open-api"]},"install":[{"id":"npm","kind":"node","package":"mineru-open-api","bins":["mineru-open-api"],"label":"Install via npm"},{"id":"uv","kind":"uv","package":"mineru-open-api","bins":["mineru-open-api"],"label":"Install via uv"},{"id":"go","kind":"go","package":"github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api","bins":["mineru-open-api"],"label":"Install via go install","os":["darwin","linux"]}]}}
---

# PPTX to Markdown - Extract Slides

Convert Word, PowerPoint, and Excel files to Markdown using MinerU Open API. No API key required.

## Quick Start

```bash
# PPTX to Markdown - Extract Slides
mineru-open-api flash-extract report.docx

# PPTX to Markdown - Extract Slides
mineru-open-api flash-extract slides.pptx

# PPTX to Markdown - Extract Slides
mineru-open-api flash-extract data.xlsx

# PPTX to Markdown - Extract Slides
mineru-open-api flash-extract https://example.com/report.docx

# PPTX to Markdown - Extract Slides
mineru-open-api flash-extract report.docx -o ./output/
```

## Language Rule

You MUST reply to the user in the SAME language they use. This is non-negotiable.

## Capabilities

- Converts DOCX, PPTX, XLS, XLSX to Markdown
- Supports both local files and URLs directly
- Preserves text, tables, and document structure
- No API key, no signup, no authentication
- Max 10MB / 20 pages per document

## When to Use

- User asks to "read", "extract", or "convert" a Word/PowerPoint/Excel file
- User shares a .docx, .pptx, or .xlsx and asks for its content
- User wants to summarize or analyze an office document
- User needs document content in Markdown format

## CLI Reference

Run `mineru-open-api flash-extract --help` for all available options.

## Data Privacy

- `flash-extract` uploads the document to MinerU's cloud API for processing and returns the result. No account or API key is required.
- Documents are processed in real-time and are not stored after extraction.
- For details, see https://mineru.net

## Notes

- Output is Markdown only; embedded images may be replaced with placeholders
- For larger files (up to 200MB/600 pages) or precision extraction, use `mineru-open-api extract` (requires auth via `mineru-open-api auth`)
- If the CLI cannot be installed via npm/uv/go, download it from https://mineru.net/ecosystem?tab=cli
