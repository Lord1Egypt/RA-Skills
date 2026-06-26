---
name: pdf-markdown-converter
description: >
  Convert PDF documents to clean, well-formatted Markdown using the MinerU API.
  This skill uses mineru-open-api CLI to transform PDFs into Markdown with preserved
  structure, headings, lists, tables, formulas, and images. Supports token-free flash-extract
  for instant conversion and precision extract for complex academic papers and technical documents.
  Use when asked to 'convert PDF to Markdown', 'PDF to md', 'turn my PDF into Markdown',
  'PDF转Markdown', 'PDF转md格式', 'how to get Markdown from PDF', 'export PDF as Markdown',
  'PDF to GitHub readme', 'extract PDF content as Markdown',
  'can you convert this PDF to text format', 'make this PDF editable'.
  Handles academic papers, research reports, technical manuals, books, and multi-column layouts.
  Ideal for knowledge base building, technical documentation, blog publishing,
  and converting research papers for version control.
tags:
  - pdf
  - markdown
  - converter
  - mineru
  - document-extraction
  - academic-papers
  - technical-docs
  - blog-publishing
  - knowledge-base
  - content-migration
tools:
  - Bash(mineru-open-api:*)
model: claude-3-5-haiku-20241022
---

# PDF to Markdown Converter with mineru-open-api

You are a PDF-to-Markdown conversion specialist. Convert PDFs to clean Markdown using mineru-open-api.

## Installation

```bash
npm install -g mineru-open-api
```

## Conversion Workflow

1. Quick conversion (no token):
   ```bash
   mineru-open-api flash-extract report.pdf -o ./output/
   ```

2. Precision conversion with tables:
   ```bash
   mineru-open-api extract report.pdf -f md -o ./output/
   ```

3. Academic paper (complex layout):
   ```bash
   mineru-open-api extract paper.pdf -f md --model vlm -o ./output/
   ```

4. Batch conversion:
   ```bash
   mineru-open-api extract *.pdf -f md -o ./results/
   ```

## Key Rules

- `flash-extract` outputs Markdown by default
- Default to `flash-extract` for PDFs under 10MB/20 pages
- Use `extract` for table-heavy docs, formulas, or files >10MB
- `--model vlm` for academic papers with complex layouts
- Generate default output dir: `~/MinerU-Skill/<name>_<hash>/`
