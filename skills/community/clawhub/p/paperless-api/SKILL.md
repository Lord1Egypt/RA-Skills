---
name: paperless-api
description: Upload and categorize documents using the Paperless-ngx API. Use for automating document management tasks with your Paperless-ngx instance.
---

# Paperless API Skill

This skill provides tools for interacting with your Paperless-ngx instance, specifically for uploading and categorizing documents.

## Configuration

To use this skill, you need to provide your Paperless-ngx host URL and an API key.

- **Host URL:** Your Paperless-ngx instance URL (e.g., `http://192.168.1.17:30070`)
- **API Key:** Your Paperless-ngx API key (e.g., `71ca2b0f4af4eeaec40e54832ed878ef30d1e053`)

## Usage

### Uploading and Categorizing Documents

Use the `upload_document.py` script to upload a document and optionally assign tags or a document type.

**Script:** `scripts/upload_document.py`

**Arguments:**

- `--file_path`: Path to the document file to upload (e.g., `/path/to/invoice.pdf`)
- `--host`: Your Paperless-ngx host URL
- `--api_key`: Your Paperless-ngx API key
- `--title`: (Optional) Title for the document
- `--tags`: (Optional) Comma-separated list of tags (e.g., `"invoice,paid"`)
- `--document_type`: (Optional) Document type name (e.g., `"Invoice"`)

**Example:**

```bash
python scripts/upload_document.py \
  --file_path /path/to/my_document.pdf \
  --host http://192.168.1.17:30070 \
  --api_key 71ca2b0f4af4eeaec40e54832ed878ef30d1e053 \
  --title "My Important Document" \
  --tags "important,work" \
  --document_type "Contract"
```

## API Endpoints

For detailed API endpoint information, refer to `references/api_endpoints.md`. (This file will contain specific API routes once we have more information.)
