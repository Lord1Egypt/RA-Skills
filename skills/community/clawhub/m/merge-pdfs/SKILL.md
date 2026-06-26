---
name: merge-pdfs
description: "Combine two or more PDFs into a single document. Supports URLs, base64, multipart uploads, and custom metadata."
---

# Merge PDFs

## What It Does
Combines two or more PDFs into a single document. Google Drive share links are automatically converted to direct-download URLs.

## When to Use
- Combine multiple PDF invoices, reports, or contracts into one file
- Merge chapters or sections into a single document

## Required Inputs
Provide one of:
- `urls` — array of PDF URLs (2-25)
- `files` — array of base64-encoded PDFs
- Multipart upload with `files` field(s)

## Authentication
Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

## Use Cases
- **Invoice Bundling** — Combine monthly invoices into a single PDF for clients
- **Report Assembly** — Merge cover page, table of contents, and report chapters into one document
- **Legal Document Packets** — Bundle contracts, appendices, and exhibits into one filing
- **Student Submissions** — Merge multiple assignment PDFs into one submission file
- **Mortgage/Loan Packages** — Combine application forms, ID scans, and financial docs into one package
- **Book Assembly** — Merge individual chapter PDFs into a complete manuscript

## Limits
| Constraint | Value |
|------------|-------|
| Max input files | 25 |
| Max pages per document | 200 |
| Max total pages | 500 |
| Max input file size | 50 MB |
| Download timeout | 60 s |

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/pdf/merge \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://pdfapihub.com/sample.pdf",
      "https://pdfapihub.com/sample1.pdf"
    ],
    "output": "url"
  }'
```
