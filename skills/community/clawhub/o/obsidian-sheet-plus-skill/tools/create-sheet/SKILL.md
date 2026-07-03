---
name: obsidian-sheet-plus-create-sheet
description: Use when creating a new worksheet in the Obsidian workbook — for adding data categories, dashboard pages, or report sections
---

# create-sheet
Create a new worksheet in the workbook. The new worksheet is blank by default and can be populated later via set-sheet-data.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/create_sheet` |
| Auth | None by default. Requires `X-API-KEY` header when enabled |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | Yes | - | Name of the new worksheet; must not duplicate an existing sheet name |

## Response
```json
{
  "success": true,
  "data": {
    "id": "sheet-xxx",
    "name": "Dashboard",
    "workbookId": "wb-xxx"
  }
}
```

## Example
```bash
curl -X POST http://127.0.0.1:3000/create_sheet \
  -H "Content-Type: application/json" \
  -d '{"sheetName": "Dashboard"}'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Sheet already exists` | The worksheet name is already in use | Use a different name, or delete the old sheet first |
| `No active workbook` | No spreadsheet file is currently open | Open a .sheet file in Obsidian |
| Name contains special characters | sheetName uses unsupported special characters | Use letters, numbers, Chinese characters, and underscores |
