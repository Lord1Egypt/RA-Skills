---
name: pdf-ocr-parse
description: "Extract text from scanned PDFs using Tesseract OCR. Supports multiple languages, page selection, DPI control, and word-level bounding boxes."
---

# PDF OCR Parse

## What It Does
Rasterises each selected page of a PDF at the given DPI, then runs Tesseract OCR on each page image. Returns per-page text with confidence scores, and optionally per-word bounding boxes.

## When to Use
- Extract text from scanned PDF documents
- OCR invoices, receipts, or legacy documents in PDF format
- Extract digits-only data (invoice amounts) with char_whitelist
- Process multi-language documents

## Required Inputs
Provide one of:
- `url` — URL to a scanned PDF
- `base64_pdf` — base64-encoded PDF
- Multipart upload with `file` field

## Authentication
Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

## Use Cases
- **Scanned Invoice Processing** — OCR scanned PDF invoices to extract text for accounting systems
- **Legacy Document Digitization** — Convert old scanned paper documents into searchable text
- **Insurance Claims** — Extract text from scanned claim forms and medical documents
- **Legal Discovery** — OCR scanned legal documents for full-text search and review
- **Multi-Language Documents** — Process documents in Hindi, French, German, etc. with language-specific models
- **Form Digitization** — Extract filled field values from scanned paper forms

## Tesseract Configuration
| Param | Default | Description |
|-------|---------|-------------|
| `lang` | `eng` | Language code(s), `+` separated |
| `psm` | `3` | Page segmentation mode (0–13) |
| `oem` | `3` | OCR engine mode (0=legacy, 1=LSTM, 3=default) |
| `dpi` | `200` | Rasterisation DPI (72–400) |
| `char_whitelist` | — | Restrict to specific characters |

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/pdf/ocr/parse \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://pdfapihub.com/sample-pdfinvoice-with-image.pdf",
    "pages": "1-3",
    "lang": "eng",
    "dpi": 300,
    "detail": "words"
  }'
```
