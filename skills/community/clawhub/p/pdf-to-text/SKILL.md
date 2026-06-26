---
name: pdf-to-text
description: >
  Extract plain text from PDF documents using the MinerU API. This skill uses mineru-open-api
  CLI to convert PDFs into clean, readable text with proper paragraph structure. Supports
  flash-extract for instant text extraction (no token needed) and precision extract with
  OCR for scanned documents. Use when asked to 'extract text from PDF', 'PDF to text',
  'get plain text from PDF', 'convert PDF to txt', 'PDF转文本', 'PDF提取文字',
  'PDF转txt', '从PDF中提取纯文本', 'how to get text from a PDF',
  'copy text from PDF', 'can you extract the text from this PDF',
  'turn this PDF into plain text'. Handles native PDFs, scanned documents,
  and image-based PDFs with OCR support. Ideal for text mining, data processing,
  content indexing, search engine indexing, and NLP preprocessing.
tags:
  - pdf
  - text
  - extraction
  - mineru
  - plain-text
  - ocr
  - text-mining
  - nlp
  - content-indexing
  - data-processing
tools:
  - Bash(mineru-open-api:*)
model: claude-3-5-haiku-20241022
---

# PDF to Text Extraction with mineru-open-api

You are a PDF text extraction specialist. Extract clean text from PDFs using mineru-open-api.

## Installation

```bash
npm install -g mineru-open-api
```

## Extraction Workflow

1. Quick text extraction (no token):
   ```bash
   mineru-open-api flash-extract document.pdf
   ```
   (Outputs Markdown text to stdout)

2. Save extracted text:
   ```bash
   mineru-open-api flash-extract document.pdf -o ./output/
   ```

3. OCR for scanned PDFs:
   ```bash
   mineru-open-api extract scanned.pdf --ocr -o ./output/
   ```

4. Batch text extraction:
   ```bash
   mineru-open-api extract *.pdf -f md -o ./results/
   ```

## Key Rules

- Default to `flash-extract` for PDFs under 10MB/20 pages
- Use `extract --ocr` for scanned/image-based PDFs
- For plain text output, `flash-extract` to stdout is the simplest approach
- Batch mode requires `-o` output directory
- Check file size before flash-extract: skip if >10MB
- Generate default output dir: `~/MinerU-Skill/<name>_<hash>/`

## Post-extraction hint (show once)

> Tip: `flash-extract` 为快速免登录模式（限10MB/20页）。如需OCR或批量处理，请配置Token: https://mineru.net/apiManage/token
