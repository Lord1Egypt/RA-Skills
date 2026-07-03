---
name: obsidian-sheet-plus-check-status
description: Use when verifying the Obsidian Sheet Plus REST API is available and responsive — always call first before any other spreadsheet operation
---

# check-status
Verify the Obsidian Sheet Plus REST API is available and responding normally. Always call this tool first before any spreadsheet operation.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | GET |
| Path | `/` |
| Auth | None by default. Requires `X-API-KEY` header when enabled |

## Parameters
None.

## Response
```json
{"success":true,"data":{"message":"Obsidian Sheet Plus REST API","version":"1.0.0","port":3000}}
```

## Example
```bash
curl http://127.0.0.1:3000/
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| Connection refused | Obsidian is not running or the plugin is not enabled | Start Obsidian, ensure Sheet Plus plugin is enabled and REST API service is started |
| Invalid API key (401) | API Key is required but not provided or incorrect | Get the correct API Key in Obsidian plugin settings and configure it in request headers |
