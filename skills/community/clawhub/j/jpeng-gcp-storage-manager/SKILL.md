---
name: jpeng-gcp-storage-manager
description: "Manage Google Cloud Storage"
version: "1.0.0"
author: "jpeng"
tags: ["gcp", "storage", "cloud"]
---

# GCP Storage Manager

Manage Google Cloud Storage

## When to Use

- User needs gcp related functionality
- Automating storage tasks
- Cloud operations

## Usage

```bash
python3 scripts/gcp_storage_manager.py --input <input> --output <output>
```

## Configuration

Set required environment variables:

```bash
export STORAGE_API_KEY="your-api-key"
```

## Output

Returns JSON with results:

```json
{
  "success": true,
  "data": {}
}
```
