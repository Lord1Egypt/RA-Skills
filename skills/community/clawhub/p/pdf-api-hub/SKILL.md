---
name: PDF API Hub
slug: pdf-api-hub
version: 1.0.0
homepage: https://pdfapihub.com/
description: "Use when: integrating with PDF API Hub REST APIs for document automation — HTML/URL to PDF, merge, split, compress, OCR, watermark, sign, lock/unlock, convert, screenshot, parse, and file management via pdfapihub.com."
metadata: {"clawdbot":{"emoji":"📑","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

User needs to call PDF API Hub endpoints (`pdfapihub.com/api/v1/...`) for document automation: generating PDFs from HTML/URLs, merging, splitting, compressing, OCR, watermarking, signing, encrypting/decrypting, converting between PDF and images, parsing/extracting text and tables, or managing uploaded files.

## Scope

This skill ONLY:
- Provides endpoint reference, request/response contracts, and integration patterns for the PDF API Hub REST API
- Shows code examples in multiple languages (cURL, Python, Node.js, etc.)
- Explains authentication, error handling, and output format options

This skill NEVER:
- Executes API calls or generates files directly
- Stores or transmits API keys
- Accesses files outside the user's working directory

All code examples are reference patterns for the user to implement.

## Quick Reference

| Topic | File |
|-------|------|
| All endpoints & parameters | `endpoints.md` |
| Code examples by use case | `examples.md` |
| Advanced workflows | `advanced.md` |

## Authentication

Every request requires the `CLIENT-API-KEY` header.

```
CLIENT-API-KEY: <your-api-key>
Content-Type: application/json
```

Get your API key at [pdfapihub.com/signup](https://pdfapihub.com/signup).

## Base URL

```
https://pdfapihub.com/api/v1/
```

All endpoints use **POST** with JSON body.

## Endpoint Map

| # | Category | Endpoint | Path | What it does |
|---|----------|----------|------|--------------|
| 1 | Document | Generate PDF | `/generatePdf` | Render HTML or capture any webpage as a PDF |
| 2 | Document | Parse PDF | `/pdf/parse` | Extract text, tables, or structured layout data |
| 3 | Document | Merge PDFs | `/pdf/merge` | Combine multiple PDFs into one |
| 4 | Document | Split PDF | `/pdf/split` | Split a PDF into pages, ranges, or chunks |
| 5 | Document | Compress PDF | `/compressPdf` | Shrink file size (4 compression levels) |
| 6 | Document | PDF Info | `/pdf/info` | Get metadata and page info from a PDF |
| 7 | Document | Watermark | `/watermark` | Overlay text/logo watermarks on pages |
| 8 | Document | Sign PDF | `/sign-pdf` | Stamp a signature image on PDF pages |
| 9 | Security | Lock PDF | `/lockPdf` | AES-256 encryption with granular permissions |
| 10 | Security | Unlock PDF | `/unlockPdf` | Remove password protection |
| 11 | Conversion | Generate Image | `/generateImage` | Capture URL/HTML as PNG image |
| 12 | Conversion | Compress Image | `/compressImage` | Reduce image file size |
| 13 | Conversion | PDF to Image | `/pdfToImage` | Render PDF pages as PNG/JPG/WebP |
| 14 | Conversion | Image to PDF | `/imageToPdf` | Combine images into a PDF |
| 15 | OCR | PDF OCR | `/pdfOcr` | Extract text from scanned PDF documents |
| 16 | OCR | Image OCR | `/imageOcr` | Extract text from photos/images |
| 17 | Utility | URL to HTML | `/urlToHtml` | Fetch fully-rendered HTML via headless browser |
| 18 | File Mgmt | Upload File | `/uploadFile` | Upload a file to cloud storage |
| 19 | File Mgmt | List Files | `/listFiles` | List uploaded files |
| 20 | File Mgmt | Delete File | `/deleteFile` | Delete an uploaded file |
| 21 | Templates | Create Template | `/createTemplate` | Save a reusable HTML template |
| 22 | Templates | List Templates | `/listTemplates` | List saved templates |
| 23 | Templates | Delete Template | `/deleteTemplate` | Delete a saved template |

## Output Formats

Most endpoints support the `output_format` parameter:

| Value | Description |
|-------|-------------|
| `url` | Returns a hosted CDN URL (default) |
| `file` | Returns the file as a download |
| `base64` | Returns base64-encoded content |
| `binary` | Returns raw binary stream |
| `pdf` | Returns PDF file directly |

## Error Handling

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 400 | Invalid Request | Check JSON body shape and required fields |
| 401 | Unauthorized | Verify `CLIENT-API-KEY` header |
| 422 | Validation Failed | Check URL/HTML/options for conflicts |
| 429 | Rate Limited | Back off and retry with exponential delay |
| 500 | Internal Error | Retry; contact support if persistent |

## Common Response Shape

```json
{
  "success": true,
  "pdf_url": "https://cdn.pdfapihub.com/pdf/a1b2c3d4.pdf",
  "file_size_bytes": 84321,
  "file_deletion_date": "2026-05-04",
  "source_type": "html"
}
```

## Core Rules

### 1. Always Set output_format Explicitly

```json
{ "output_format": "url" }
```

Don't rely on defaults — be explicit about whether you need a URL, file, or base64.

### 2. Use html_content for Dynamic Documents

```json
{
  "html_content": "<h1>Invoice #{{number}}</h1>",
  "css_content": "h1 { color: #333; }",
  "dynamic_params": { "number": "INV-001" }
}
```

### 3. Use url for Webpage Capture

```json
{
  "url": "https://example.com/report",
  "wait_until": "networkidle",
  "paper_size": "A4"
}
```

### 4. Handle Files via URL or Upload

For endpoints that operate on existing PDFs (merge, split, compress, etc.), provide files via:
- Direct URL to the PDF
- Previously uploaded file reference via the Upload File endpoint

### 5. Validate Responses

Always check `success: true` in the response before using the result.

## Common Traps

| Trap | Consequence | Fix |
|------|-------------|-----|
| Missing `CLIENT-API-KEY` header | 401 error | Always include the header |
| Sending both `url` and `html_content` | Undefined behavior | Use one or the other |
| Not setting `wait_until` for SPAs | Incomplete capture | Use `networkidle` for JS-heavy pages |
| Ignoring `file_deletion_date` | Broken links after expiry | Download/store files before deletion |
| Large HTML without pagination | Timeout or huge PDF | Use `page_size` to limit output |

## Security & Privacy

- All API calls go to `pdfapihub.com` over HTTPS
- API keys should be stored in environment variables, never hardcoded
- Files hosted on CDN have an expiration date — download promptly
- This skill provides reference patterns only; it does not execute code or store credentials

## Feedback

- Full docs: [pdfapihub.com/docs](https://pdfapihub.com/docs)
- Get API key: [pdfapihub.com/signup](https://pdfapihub.com/signup)
