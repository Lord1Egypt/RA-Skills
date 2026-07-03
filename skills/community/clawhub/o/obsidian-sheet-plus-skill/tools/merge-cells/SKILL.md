---
name: obsidian-sheet-plus-merge-cells
description: Use when combining multiple adjacent cells into one — for creating headers, labels, or unified cell areas spanning multiple rows/columns
---

# merge-cells
Merges cells within a specified range into a single large cell spanning rows/columns. Useful for creating headers, labels, or unified areas.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/merge_cells` |
| Auth | None by default. When enabled, requires `X-API-KEY` header |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active sheet | Target sheet name |
| range | string | Yes | - | Cell range to merge, e.g. `A1:B2` |

> **Note**: Only the top-left cell's value is preserved after merging; other cell contents will be lost. Use unmerge-cells to undo merges.

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
curl -X POST http://127.0.0.1:3000/merge_cells \
  -H "Content-Type: application/json" \
  -d '{"sheetName":"Sheet1","range":"A1:B2"}'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Sheet not found` | Sheet name does not exist | Call get-sheet-list first to confirm the correct sheet name |
| `Range is invalid` | Invalid range format | Use A1 notation (e.g. `A1:C10`), row numbers start at 1 |
| `No active workbook` | No spreadsheet file is currently open | Open a .sheet file in Obsidian |
| Merge failed | Range contains already merged cells | Call unmerge-cells first to undo existing merges, then re-merge |
