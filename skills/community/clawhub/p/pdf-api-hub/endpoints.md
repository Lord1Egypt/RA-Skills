# PDF API Hub — Endpoint Reference

All endpoints use `POST https://pdfapihub.com/api/v1/{endpoint}` with `CLIENT-API-KEY` header.

---

## Document APIs

### Generate PDF — `/generatePdf`

Render HTML or capture any webpage as a pixel-perfect PDF.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| url | string | Conditional | Webpage URL (required if no `html_content`) | `https://example.com` |
| html_content | string | Conditional | Raw HTML (required if no `url`) | `<h1>Hello</h1>` |
| css_content | string | No | CSS styles (used with `html_content`) | `h1{font-size:32px;}` |
| paper_size | string | No | A0–A6, Letter, Legal, Tabloid, Ledger. Default: A4 | `A4` |
| landscape | boolean | No | Landscape orientation | `false` |
| print_background | boolean | No | Include CSS backgrounds. Default: true | `true` |
| displayHeaderFooter | boolean | No | Show header/footer | `false` |
| preferCSSPageSize | boolean | No | Prefer CSS `@page` size over `paper_size` | `false` |
| margin | string/object | No | Preset (`none`/`small`/`medium`/`large`) or object `{top,right,bottom,left}` | `"medium"` |
| viewPortWidth | integer | No | Viewport width. Default: 1080 | `1080` |
| viewPortHeight | integer | No | Viewport height. Default: 720 | `720` |
| font | string | No | Google Font names, pipe-separated | `"Inter\|Roboto"` |
| wait_until | string | No | `load`, `domcontentloaded`, `networkidle`, `commit` | `"load"` |
| wait_till | integer | No | Extra delay in seconds after page load | `2` |
| cookie_accept_text | string | No | Cookie consent button text to auto-click (URL mode) | `"Accept ALL"` |
| dynamic_params | object | No | Key-value pairs for `{{placeholder}}` substitution in HTML | `{"name":"Rishabh"}` |
| page_size | integer | No | Max pages to return (capped by plan) | `10` |
| output_format | string | No | `url` (default), `file`, `base64`, `binary`, `pdf` | `"url"` |
| output_filename | string | No | Custom output filename | `"report.pdf"` |

**Response:**
```json
{
  "success": true,
  "pdf_url": "https://cdn.pdfapihub.com/pdf/a1b2c3d4.pdf",
  "file_size_bytes": 84321,
  "file_deletion_date": "2026-05-04",
  "source_type": "html"
}
```

---

### Parse / Extract PDF — `/pdf/parse`

Pull text, tables, or structured layout data from any PDF.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| url | string | Conditional | URL of the PDF to parse | `https://example.com/doc.pdf` |
| file | file | Conditional | Uploaded PDF file | — |
| extract_type | string | No | `text`, `tables`, `layout` | `"text"` |
| pages | string | No | Page range to extract | `"1-5"` |
| output_format | string | No | `url`, `file`, `base64` | `"url"` |

---

### Merge PDFs — `/pdf/merge`

Combine multiple PDFs into a single document.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| urls | array | Yes | Array of PDF URLs to merge | `["url1.pdf","url2.pdf"]` |
| output_format | string | No | `url`, `file`, `base64` | `"url"` |
| output_filename | string | No | Custom output filename | `"merged.pdf"` |

---

### Split PDF — `/pdf/split`

Split a PDF into pages, ranges, or equal chunks.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| url | string | Yes | URL of the PDF to split | `https://example.com/doc.pdf` |
| pages | string | No | Page ranges (e.g., `"1-3,5,7-9"`) | `"1-5"` |
| split_every | integer | No | Split into chunks of N pages | `2` |
| output_format | string | No | `url`, `file`, `base64` | `"url"` |

---

### Compress PDF — `/compressPdf`

Shrink PDF file size with configurable compression levels.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| url | string | Yes | URL of the PDF to compress | `https://example.com/doc.pdf` |
| compression_level | string | No | `low`, `medium`, `high`, `max` | `"medium"` |
| output_format | string | No | `url`, `file`, `base64` | `"url"` |

---

### PDF Info — `/pdf/info`

Get metadata and page information from a PDF.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| url | string | Yes | URL of the PDF | `https://example.com/doc.pdf` |

---

### Watermark — `/watermark`

Overlay text or logo watermarks on every page.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| url | string | Yes | URL of the PDF to watermark | `https://example.com/doc.pdf` |
| text | string | Conditional | Watermark text | `"CONFIDENTIAL"` |
| image_url | string | Conditional | Watermark image URL | `https://example.com/logo.png` |
| position | string | No | Placement position | `"center"` |
| opacity | number | No | Watermark opacity (0–1) | `0.3` |
| output_format | string | No | `url`, `file`, `base64` | `"url"` |

---

### Sign PDF — `/sign-pdf`

Stamp a signature image on PDF pages.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| url | string | Yes | URL of the PDF to sign | `https://example.com/doc.pdf` |
| signature_url | string | Yes | URL of the signature image | `https://example.com/sig.png` |
| position | string | No | Signature placement | `"bottom-right"` |
| pages | string | No | Pages to sign | `"last"` |
| output_format | string | No | `url`, `file`, `base64` | `"url"` |

---

## Security APIs

### Lock PDF — `/lockPdf`

Add AES-256 encryption with granular permissions.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| url | string | Yes | URL of the PDF to lock | `https://example.com/doc.pdf` |
| password | string | Yes | Password for encryption | `"securePass123"` |
| permissions | object | No | Granular permissions (print, copy, edit) | `{"print":true,"copy":false}` |
| output_format | string | No | `url`, `file`, `base64` | `"url"` |

### Unlock PDF — `/unlockPdf`

Remove password protection from a PDF.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| url | string | Yes | URL of the locked PDF | `https://example.com/locked.pdf` |
| password | string | Yes | Current password | `"securePass123"` |
| output_format | string | No | `url`, `file`, `base64` | `"url"` |

---

## Conversion APIs

### Generate Image — `/generateImage`

Capture full-page screenshots or render HTML to PNG with retina support.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| url | string | Conditional | Webpage URL to screenshot | `https://example.com` |
| html_content | string | Conditional | HTML to render as image | `<h1>Hello</h1>` |
| css_content | string | No | CSS styles | `h1{color:red;}` |
| viewPortWidth | integer | No | Viewport width | `1920` |
| viewPortHeight | integer | No | Viewport height | `1080` |
| full_page | boolean | No | Capture full scrollable page | `true` |
| image_format | string | No | `png`, `jpg`, `webp` | `"png"` |
| output_format | string | No | `url`, `file`, `base64` | `"url"` |

### Compress Image — `/compressImage`

Reduce image file size.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| url | string | Yes | URL of the image | `https://example.com/photo.png` |
| quality | integer | No | Compression quality (1–100) | `80` |
| output_format | string | No | `url`, `file`, `base64` | `"url"` |

### PDF to Image — `/pdfToImage`

Render PDF pages as PNG/JPG/WebP images.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| url | string | Yes | URL of the PDF | `https://example.com/doc.pdf` |
| pages | string | No | Pages to convert | `"1-3"` |
| image_format | string | No | `png`, `jpg`, `webp` | `"png"` |
| dpi | integer | No | Resolution (dots per inch) | `300` |
| background_color | string | No | Background color | `"#ffffff"` |
| output_format | string | No | `url`, `file`, `base64` | `"url"` |

### Image to PDF — `/imageToPdf`

Combine images into a PDF with page size, orientation, and fit mode.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| urls | array | Yes | Array of image URLs | `["img1.png","img2.jpg"]` |
| paper_size | string | No | Page size. Default: A4 | `"A4"` |
| landscape | boolean | No | Landscape orientation | `false` |
| fit_mode | string | No | How images fit the page | `"contain"` |
| output_format | string | No | `url`, `file`, `base64` | `"url"` |

---

## OCR APIs

### PDF OCR — `/pdfOcr`

Extract text from scanned PDF documents.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| url | string | Yes | URL of the scanned PDF | `https://example.com/scan.pdf` |
| language | string | No | OCR language: `eng`, `por`, `rus`, or custom | `"eng"` |
| pages | string | No | Pages to OCR | `"1-5"` |
| output_format | string | No | `url`, `file`, `base64` | `"url"` |

### Image OCR — `/imageOcr`

Extract text from photos and images.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| url | string | Yes | URL of the image | `https://example.com/photo.png` |
| language | string | No | OCR language | `"eng"` |
| output_format | string | No | `url`, `file`, `base64` | `"url"` |

---

## Utility APIs

### URL to HTML — `/urlToHtml`

Fetch fully-rendered HTML from any URL using a headless browser (SPA-friendly).

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| url | string | Yes | URL to scrape | `https://example.com` |
| wait_until | string | No | `load`, `domcontentloaded`, `networkidle` | `"networkidle"` |

---

## File Management APIs

### Upload File — `/uploadFile`

Upload a file to cloud storage for use in other endpoints.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| file | file | Yes | File to upload (multipart/form-data) | — |

### List Files — `/listFiles`

List all uploaded files.

*No parameters required.*

### Delete File — `/deleteFile`

Delete an uploaded file.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| file_id | string | Yes | ID of the file to delete | `"abc123"` |

---

## Template APIs

### Create Template — `/createTemplate`

Save a reusable HTML template with dynamic placeholders.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| name | string | Yes | Template name | `"invoice-v1"` |
| html_content | string | Yes | HTML with `{{placeholder}}` variables | `<h1>{{title}}</h1>` |
| css_content | string | No | CSS styles for the template | `h1{color:#333;}` |

### List Templates — `/listTemplates`

List all saved templates.

*No parameters required.*

### Delete Template — `/deleteTemplate`

Delete a saved template.

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| template_id | string | Yes | ID of the template to delete | `"tpl_abc123"` |
