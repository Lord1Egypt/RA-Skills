---
name: pdf-to-image
description: "Convert PDF pages to images (PNG, JPG, or WebP). Supports DPI control, resize, background color, and page selection."
---

# PDF to Image

## What It Does
Renders selected pages of a PDF as images in PNG, JPG, or WebP format. Supports DPI control, resize dimensions, background color fill, and multiple output modes.

## When to Use
- Generate thumbnail previews of PDF pages
- Convert PDF pages to images for social media (OG images)
- Create high-DPI images for print
- Extract specific pages as images

## Required Inputs
Provide one of:
- `url` — public URL to a PDF
- `file` — base64-encoded PDF
- Multipart upload with `file` field

## Authentication
Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

## Use Cases
- **PDF Thumbnails** — Generate preview thumbnails for document management systems
- **Social Media Previews** — Create OG images (1200×630) from the first page of a PDF
- **E-commerce Product Sheets** — Convert product PDF spec sheets into gallery images
- **Document Previews** — Show image previews of PDFs in web apps without embedding a PDF viewer
- **Print-Ready Exports** — Export PDF pages as high-DPI images for print workflows
- **Slide Extraction** — Extract individual slides from PDF presentations as images

## Key Options
| Parameter | Description |
|-----------|-------------|
| `page` / `pages` | Single page or range (e.g. `"1-5"`) |
| `image_format` | `png` (default), `jpg`, `webp` |
| `dpi` | 72–300 (default 150) |
| `width` / `height` | Resize output dimensions |
| `background_color` | Fill transparent areas (hex) |
| `output` | `url`, `base64`, `both`, `file` |

## Limits
- Max 100 pages per request
- DPI range: 72–300
- Max resize dimension: 10000 px

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/convert/pdf/image \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://pdfapihub.com/sample-pdfapi-intro.pdf",
    "pages": "1-3",
    "image_format": "jpg",
    "dpi": 200,
    "output": "url"
  }'
```
