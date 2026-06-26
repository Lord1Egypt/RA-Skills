---
name: PDF to PowerPoint
description: Converts PDF documents into editable PowerPoint presentations with intelligent content extraction and formatting.
---

# Overview

PDF to PowerPoint is a document conversion API that transforms static PDF files into dynamic, editable PowerPoint presentations. This tool intelligently extracts text, images, and layout information from PDF documents and reconstructs them in PPTX format, preserving structure and visual hierarchy while enabling further customization.

The service is designed for professionals who need to repurpose PDF content into presentation-ready formats. Whether you're converting reports, whitepapers, or structured documents, this API handles the conversion pipeline end-to-end, reducing manual reformatting time and maintaining content integrity throughout the process.

Ideal users include business analysts, consultants, educators, and content teams who regularly work with mixed document formats and require programmatic conversion capabilities as part of larger automation workflows.

## Usage

**Sample Request:**

```json
{
  "file": "<binary PDF file content>"
}
```

Upload a PDF file using multipart/form-data encoding. The file parameter should contain the raw binary data of your PDF document.

**Sample Response:**

```json
{
  "status": "success",
  "message": "PDF conversion completed",
  "output_file": "document_converted.pptx",
  "pages_processed": 12,
  "conversion_time_ms": 2450,
  "file_url": "https://api.mkkpro.com/files/abc123def456/document_converted.pptx"
}
```

The response includes the converted PowerPoint file URL, processing metrics, and status confirmation for download and integration.

## Endpoints

### POST /upload-pdf

Uploads and converts a PDF file to PowerPoint format.

**Method:** `POST`

**Path:** `/upload-pdf`

**Description:** Accepts a PDF document via multipart file upload and initiates the conversion process to generate an editable PowerPoint presentation.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| file | binary (file) | Yes | The PDF file to be converted. Must be a valid PDF document in binary format. |

**Request Content-Type:** `multipart/form-data`

**Response (200 - Success):**

```
Content-Type: application/json
Status: 200 OK

{
  "status": "success",
  "message": "string",
  "output_file": "string",
  "pages_processed": "integer",
  "conversion_time_ms": "integer",
  "file_url": "string"
}
```

**Response (422 - Validation Error):**

```
Content-Type: application/json
Status: 422 Unprocessable Entity

{
  "detail": [
    {
      "loc": ["string" | integer],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

Returned when the uploaded file fails validation (missing, invalid format, or corrupt PDF).

## Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

## About

ToolWeb.in — 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- 🌐 [toolweb.in](https://toolweb.in)
- 🔌 [portal.toolweb.in](https://portal.toolweb.in)
- 🤖 [hub.toolweb.in](https://hub.toolweb.in)
- 🐾 [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- 🚀 [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- 📺 [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

## References

- **Kong Route:** `https://api.mkkpro.com/creative/pdf-to-pptx`
- **API Docs:** `https://api.mkkpro.com:8001/docs`
