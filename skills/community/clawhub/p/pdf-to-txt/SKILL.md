---
name: pdf-to-txt
description: "Extract plain text from all or selected pages of a PDF."
---

# PDF to Text

## What It Does
Extracts plain text from all or selected pages of a PDF.

## When to Use
- Extract readable text from a PDF for processing or analysis
- Get raw text content from PDF documents

## Required Inputs
Provide one of:
- `url` — public URL to a PDF
- `file` — base64-encoded PDF
- Multipart upload with `file` field

## Authentication
Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

## Use Cases
- **Full-Text Search Indexing** — Extract text from PDFs to build searchable indexes
- **AI/LLM Processing** — Extract PDF text for feeding into language models or chatbots
- **Content Migration** — Pull text from legacy PDF documents for migration to new systems
- **Plagiarism Detection** — Extract text for comparison and duplicate detection
- **Accessibility** — Extract text from PDFs for screen readers or text-to-speech

## Aliases
- `/v1/convert/pdf/text` is an alias

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/convert/pdf/txt \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{ "url": "https://pdfapihub.com/sample-pdfapi-intro.pdf", "output": "url" }'
```
