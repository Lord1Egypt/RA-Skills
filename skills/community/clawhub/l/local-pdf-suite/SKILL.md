---
name: pdf-toolkit
version: 1.0.3
description: "Complete local PDF toolkit — OCR, merge, split, compress, watermark, convert, and 30+ operations via Stirling-PDF API."
---

# PDF Toolkit

Local PDF processing suite powered by [Stirling-PDF](https://github.com/Stirling-Tools/Stirling-PDF). All operations run on your own hardware — no cloud, no uploads, data stays private.

> ⚠️ **Privacy note**: This skill sends PDFs to your Stirling-PDF instance via API. Ensure Stirling-PDF is deployed **locally or on a trusted private network** — do not point `STIRLING_BASE_URL` at a public third-party instance. Treat uploaded PDFs, passwords, and signing material as sensitive.

## About Stirling-PDF

Stirling-PDF is a powerful, open-source PDF editor that lets you edit, sign, redact, convert, and automate PDFs without sending documents to third-party services. It offers **60+ operations** including:

- **OCR** — Turn scanned images into searchable PDFs (Chinese + English supported)
- **Merge/Split** — Combine or break apart PDFs
- **Compress** — Reduce file size without quality loss
- **Convert** — PDF ↔ Word/HTML/Markdown/CSV/EPUB/PDF/A
- **Security** — Watermark, password protect, encrypt/decrypt, flatten
- **Edit** — Rotate, crop, reorder pages, add page numbers
- **Extract** — Pull images, bookmarks, metadata from PDFs

Self-hosted means your sensitive documents never leave your machine.

## Deploy with Docker

```bash
# Create directories for persistent data
mkdir -p /opt/stirling-pdf/data /opt/stirling-pdf/logs

# Run Stirling-PDF
docker run -d \
  --name stirling-pdf \
  -p 3998:8080 \
  -v /opt/stirling-pdf/data:/data \
  -v /opt/stirling-pdf/logs:/logs \
  -e DOCKER_ENABLE=true \
  -e PUID=1000 \
  -e PGID=1000 \
  -e SECURITY_INITIALLOGIN_USERNAME=admin \
  -e SECURITY_INITIALLOGIN_PASSWORD=your-password \
  --restart unless-stopped \
  frooodle/s-pdf:latest
```

Then access at `http://your-server:3998`

### First-time Setup

1. Open `http://your-server:3998` in your browser
2. Log in with the username/password set above
3. Go to **Account Settings → API Keys** → Generate a new key
4. Copy the key and set it as an environment variable:

```bash
export STIRLING_API_KEY="your-generated-api-key"
export STIRLING_BASE_URL="http://your-server:3998"
```

## Quick Reference

### Health check
```
GET /api/v1/info/health
X-API-KEY: $STIRLING_API_KEY
```

### OCR — Image/Scan to searchable PDF
```
POST /api/v1/misc/ocr-pdf
X-API-KEY: $STIRLING_API_KEY
Form: fileInput=@file.pdf, languages=chi_sim+eng
```

### Merge — Combine multiple PDFs
```
POST /api/v1/general/merge-pdfs
X-API-KEY: $STIRLING_API_KEY
Form: fileInput[]=@a.pdf, fileInput[]=@b.pdf, sortType=orderProvided
```

### Compress — Reduce file size
```
POST /api/v1/misc/compress-pdf
X-API-KEY: $STIRLING_API_KEY
Form: fileInput=@file.pdf, compressionLevel=standard
```

### Remove blank pages
```
POST /api/v1/misc/remove-blanks
X-API-KEY: $STIRLING_API_KEY
Form: fileInput=@file.pdf
Returns: ZIP containing processed PDF
```

### Convert PDF to other formats
```
POST /api/v1/convert/pdf/word     → .docx
POST /api/v1/convert/pdf/html     → .html
POST /api/v1/convert/pdf/markdown → .md
POST /api/v1/convert/pdf/csv      → .csv
POST /api/v1/convert/pdf/epub    → .epub
POST /api/v1/convert/pdf/txt     → .txt
POST /api/v1/convert/pdf/pdfa    → PDF/A (archival)
```

### Convert images to PDF
```
POST /api/v1/convert/img/pdf
X-API-KEY: $STIRLING_API_KEY
Form: fileInput=@image.jpg, colorType=color, fitOption=maintainAspectRatio
```

### Security
```
POST /api/v1/security/add-watermark  → text/image watermark
POST /api/v1/security/remove-watermark
POST /api/v1/security/encrypt        → password protect
POST /api/v1/security/decrypt        → remove password
POST /api/v1/security/flatten        → flatten annotations
POST /api/v1/security/sign            → digital signature
```

### Page operations
```
POST /api/v1/general/split-pdf       → split by page range
POST /api/v1/general/rotate-pdf     → rotate pages
POST /api/v1/general/extract-pages   → extract specific pages
POST /api/v1/general/move-pages      → reorder pages
```

### Extract
```
POST /api/v1/images/extract-images     → pull images from PDF
POST /api/v1/misc/extract-bookmarks   → extract PDF bookmarks
POST /api/v1/misc/extract-metadata    → read PDF metadata
```

### Utilities
```
POST /api/v1/general/add-page-numbers
POST /api/v1/general/rename
POST /api/v1/general/join-pdfs
POST /api/v1/general/flatten          → flatten PDF form fields
```

## Environment

Set before use:
```bash
export STIRLING_API_KEY="your-api-key"
export STIRLING_BASE_URL="http://your-server:3998"  # optional, defaults to localhost
```

## Notes
- All requests require `X-API-KEY` header
- Returns processed file or JSON error
- `remove-blanks` returns a ZIP — extract the PDF inside
- `merge` requires at least 2 files
- `ocr`: use `chi_sim+eng` for Chinese documents
- Full endpoint list: `/swagger-ui/index.html` on your instance
- OCR requires Tesseract language packs (`chi_sim` for Chinese)