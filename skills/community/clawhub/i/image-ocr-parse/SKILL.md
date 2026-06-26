---
name: image-ocr-parse
description: "Extract text from images via the PDFAPIHub cloud OCR API. Images are uploaded to pdfapihub.com for Tesseract OCR processing. Supports preprocessing (grayscale, sharpen, threshold, resize) and word-level bounding boxes. Requires a CLIENT-API-KEY header."
metadata: {"openclaw": {"primaryEnv": "PDFAPIHUB_API_KEY", "requires": {"env": ["PDFAPIHUB_API_KEY"]}}}
---

# Image OCR Parse

## What It Does
Extracts text from images via the PDFAPIHub hosted OCR API. Your image is uploaded to PDFAPIHub servers where Tesseract OCR processes it and returns the extracted text. Supports optional image preprocessing to improve OCR quality on low-resolution or noisy inputs.

## When to Use
- Extract text from photos of receipts, signs, or documents
- OCR business cards, ID cards, or labels
- Process low-quality images with preprocessing

## Required Inputs
Provide one of:
- `image_url` — URL to an image
- `base64_image` — base64-encoded image
- Multipart upload with `file` field

## Authentication
This skill calls the PDFAPIHub hosted API at `https://pdfapihub.com/api`. Your image is uploaded to PDFAPIHub servers for OCR processing.

Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

**Privacy note:** Images you process are uploaded to PDFAPIHub's cloud service and the extracted text is returned. Do not send sensitive images unless you trust the service. Files are auto-deleted after 30 days.

## Use Cases
- **Receipt Scanning** — Extract text from receipt photos for expense tracking
- **Business Card Reader** — OCR business card images to extract name, phone, email
- **License Plate Recognition** — Extract plate numbers from photos (with char_whitelist)
- **Meter Reading** — Extract digits from utility meter photos for automated logging
- **Whiteboard Capture** — OCR whiteboard or handwritten note photos into text
- **Product Label Scanning** — Extract ingredient lists or nutrition info from product label photos

## Image Preprocessing Options
| Param | Default | Description |
|-------|---------|-------------|
| `grayscale` | false | Convert to grayscale |
| `sharpen` | false | Apply sharpening |
| `threshold` | 0 | Binarization threshold (1–255) |
| `resize` | 0 | Scale factor (max 4x) |

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/image/ocr/parse \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://pdfapihub.com/sample-invoicepage.png",
    "lang": "eng",
    "grayscale": true,
    "sharpen": true,
    "detail": "words"
  }'
```
