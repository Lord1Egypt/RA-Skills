---
name: obsidian-sheet-plus-unmerge-cells
description: Use when splitting previously merged cells back into individual cells — for restructuring or removing merged headers
---

# unmerge-cells
Splits previously merged cells within a specified range back into individual cells.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/unmerge_cells` |
| Auth | None by default. When enabled, requires `X-API-KEY` header |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active sheet | Target sheet name |
| range | string | Yes | - | Cell range to unmerge, e.g. `A1:B2` |

> **Note**: After unmerging, content from the previously merged cells is only retained in the original top-left position.

## Response
```json
{
  "success": true,
  "data": {
    "range": "A1:B2",
    "sheetName": "Sheet1"
  }
}
```

## Example
```bash
curl -X POST http://127.0.0.1:3000/unmerge_cells \
  -H "Content-Type: application/json" \
  -d '{"sheetName":"Sheet1","range":"A1:B2"}'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Sheet not found` | Sheet name does not exist | Call get-sheet-list first to confirm the correct sheet name |
| `Range is invalid` | Invalid range format | Use A1 notation (e.g. `A1:C10`), row numbers start at 1 |
| `No active workbook` | No spreadsheet file is currently open | Open a .sheet file in Obsidian |
| Unmerge failed | No merged cells exist in the range | Ensure the range actually contains merged cells |
