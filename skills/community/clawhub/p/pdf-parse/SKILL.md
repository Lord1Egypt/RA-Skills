---
name: pdf-parse
description: "Parse a PDF into structured JSON: text, layout-aware blocks with bounding boxes, tables, and image metadata."
---

# PDF Parse

## What It Does
Parses a PDF into structured JSON with text content, layout-aware blocks (with normalized bounding boxes), tables, and image metadata.

## When to Use
- Extract structured data from PDFs (text, tables, images)
- Get layout-aware content with bounding box coordinates
- Parse invoices, forms, or reports into machine-readable format

## Parsing Modes
| Mode | Description |
|------|-------------|
| `text` | Text only |
| `layout` | Text + text blocks with bounding boxes |
| `tables` | Text + table blocks |
| `full` | Text + blocks + tables + images (default) |

## Required Inputs
Provide one of:
- `url` — public URL to a PDF
- Multipart upload with `file` field

## Authentication
Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

## Use Cases
- **Invoice Parsing** — Extract line items, totals, and vendor info from PDF invoices
- **Resume Parsing** — Extract structured data (name, experience, skills) from PDF resumes
- **Contract Analysis** — Extract clauses, dates, and parties from legal PDF contracts
- **Form Data Extraction** — Pull filled form fields and values from PDF forms
- **Research Paper Analysis** — Extract text, tables, and figures from academic PDFs
- **Document Indexing** — Parse PDFs into structured JSON for search engine indexing

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/pdf/parse \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{ "url": "https://pdfapihub.com/sample-pdfinvoice-with-image.pdf", "mode": "full", "pages": "1-3" }'
```
