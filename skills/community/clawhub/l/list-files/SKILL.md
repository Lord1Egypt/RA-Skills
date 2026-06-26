---
name: list-files
description: "List all files uploaded by this API key. Returns URL and creation timestamp, ordered newest first."
---

# List Files

## What It Does
Lists all files uploaded by the authenticated API key. Returns URL and creation timestamp for each file, ordered newest first.

## When to Use
- View all files you've uploaded
- Find a specific file URL for further processing
- Check upload history

## Required Inputs
None (uses API key to identify owner).

## Optional Inputs
- `limit` — max number of files (1–500, default 100)

## Authentication
Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

## Use Cases
- **File Management Dashboard** — Display all uploaded files in a management UI
- **Audit Trail** — Review recently uploaded files for auditing purposes
- **Pipeline Monitoring** — Check which files have been processed in an automated workflow
- **Cleanup Planning** — Review uploaded files before batch deletion

## Example Usage
```bash
curl -X GET "https://pdfapihub.com/api/v1/file/list?limit=10" \
  -H "CLIENT-API-KEY: your_api_key"
```
