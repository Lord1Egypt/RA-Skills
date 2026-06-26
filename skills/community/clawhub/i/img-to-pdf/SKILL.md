---
name: image-to-pdf
description: "Combine one or more images into a single PDF document with page layout control (page size, orientation, fit mode, margin)."
---

# Image to PDF

## What It Does
Combines one or more images into a single PDF document. Supports page size selection, orientation, fit modes, and margin control.

## When to Use
- Convert scanned images into a PDF document
- Combine multiple photos/screenshots into one PDF
- Create a PDF portfolio from image files

## Required Inputs
Provide one of:
- `image_url` — single image URL
- `image_urls` — array of image URLs
- `images_base64` — array of base64-encoded images
- Multipart upload with `file` field(s)

## Authentication
Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

## Use Cases
- **Scanned Document Assembly** — Combine scanned pages into a single PDF document
- **Photo Portfolio** — Create a PDF photo book or portfolio from multiple images
- **Insurance Claims** — Bundle damage photos into one PDF for submission
- **Real Estate Listings** — Combine property photos into a downloadable PDF brochure
- **Medical Records** — Assemble scanned medical documents into a single patient file
- **ID Document Bundles** — Combine front/back scans of IDs into one PDF

## Key Options
| Parameter | Description |
|-----------|-------------|
| `page_size` | `A4`, `Letter`, `Legal`, `A3`, `A5`, or `original` |
| `orientation` | `portrait` or `landscape` |
| `fit_mode` | `fit` (default), `fill`, `stretch`, `original` |
| `margin` | Padding in points (0–200) |
| `output` | `url` (default), `base64`, `both`, `file` |

## Limits
- Max 100 images per request

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/convert/image/pdf \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "image_urls": ["https://pdfapihub.com/sample.jpg", "https://pdfapihub.com/sample-invoicepage.png"],
    "page_size": "A4",
    "orientation": "portrait",
    "fit_mode": "fit",
    "margin": 36,
    "output": "url"
  }'
```
