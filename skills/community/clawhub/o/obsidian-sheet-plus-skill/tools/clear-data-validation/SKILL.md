---
name: obsidian-sheet-plus-clear-data-validation
description: Use when removing data validation rules from cells — to allow unrestricted input after previously setting constraints
---

# clear-data-validation
Remove data validation rules from the specified range. After removal, cells return to unrestricted input mode.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/clear_data_validation` |
| Auth | None by default. Requires `X-API-KEY` header when enabled |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | Yes | - | Target worksheet name |
| range | string | Yes | - | Cell range, e.g. `A1:A10` |

## Response
```json
{
  "success": true,
  "data": {
    "range": "A1:A10"
  }
}
```

## Example
```bash
curl -X POST http://127.0.0.1:3000/clear_data_validation \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "A1:A10"
  }'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Range is invalid` | Range format is incorrect | Use A1 notation (e.g. `A1:C10`) |
| `Sheet not found` | Worksheet name does not exist | Call get-sheet-list first to confirm the sheet name |
