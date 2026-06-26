---
name: lock-pdf
description: "Add password protection and encryption to a PDF. Supports AES-256, AES-128, RC4-128 encryption and granular permissions."
---

# Lock PDF

## What It Does
Encrypts a PDF with password protection. Supports AES-256 (default), AES-128, and RC4-128 encryption. Allows setting separate user and owner passwords with granular permission controls.

## When to Use
- Protect a PDF with a password before sharing
- Set permissions (allow print but deny copy/modify)
- Re-encrypt an already encrypted PDF with a new password

## Required Inputs
- `password` — user password (required to open the PDF)
- Plus one of: `url`, `base64_pdf`, or multipart `file` upload

## Authentication
Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

## Use Cases
- **Confidential Document Protection** — Encrypt contracts, NDAs, or financial reports before sharing
- **Read-Only Distribution** — Allow viewing and printing but prevent copying or editing
- **Client Deliverables** — Password-protect reports or proposals sent to clients
- **Compliance** — Encrypt sensitive PDFs (HIPAA, GDPR) before storage or transmission
- **Exam Papers** — Lock exam PDFs with a password released only at exam time
- **IP Protection** — Restrict copying from proprietary documents while allowing viewing

## Permissions
| Permission | Description |
|-----------|-------------|
| `print` | Allow printing |
| `print_highres` | Allow high-res printing |
| `copy` | Allow copying text |
| `modify` | Allow modifying content |
| `annotate` | Allow adding annotations |
| `fill_forms` | Allow filling form fields |
| `extract` | Allow extracting content |
| `assemble` | Allow assembling pages |

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/lockPdf \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://pdfapihub.com/sample.pdf",
    "password": "viewerPass",
    "owner_password": "adminPass",
    "permissions": { "print": true, "copy": false, "modify": false },
    "output": "url"
  }'
```
