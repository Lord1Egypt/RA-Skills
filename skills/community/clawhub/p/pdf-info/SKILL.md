---
name: pdf-info
description: "Get PDF metadata, encryption status, page count, and file size. Useful for pre-flight checks before processing."
---

# PDF Info

## What It Does
Inspects a PDF and returns metadata including encryption status, page count, file size, and document properties (title, author, subject, creator).

## When to Use
- Check if a PDF is encrypted before calling unlock
- Pre-flight validation before PDF processing
- Get page count and file size information

## Required Inputs
Provide one of:
- `url` — URL to a PDF
- `base64_pdf` — base64-encoded PDF
- Multipart upload with `file` field

## Authentication
Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

## Use Cases
- **Pre-Flight Validation** — Check page count and encryption status before processing
- **Upload Validation** — Verify uploaded PDFs meet requirements (page limit, not encrypted)
- **Workflow Routing** — Route encrypted PDFs to unlock step, unencrypted directly to processing
- **Metadata Display** — Show document title, author, and page count in a document management UI
- **Quota Checks** — Verify page count before merge/split to avoid exceeding limits

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/pdf/info \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{ "url": "https://pdfapihub.com/sample.pdf" }'
```
