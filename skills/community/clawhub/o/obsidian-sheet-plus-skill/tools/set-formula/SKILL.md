---
name: obsidian-sheet-plus-set-formula
description: Use when adding Excel-style formulas (SUM, AVERAGE, IF, VLOOKUP, etc.) to cells — for calculations, aggregations, or dynamic cell values
---

# set-formula
Set a cell formula. Supports Excel-compatible formulas such as SUM, AVERAGE, IF, VLOOKUP, etc. Formulas are automatically calculated and updated.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/set_formula` |
| Auth | None by default. Requires `X-API-KEY` header when enabled |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active worksheet | Target worksheet name |
| range | string | Yes | - | Cell or range, e.g. `A1` or `A1:B10` |
| formula | string | Yes | - | Formula, must start with `=`, e.g. `=SUM(B1:B10)` |

## Response
```json
{
  "success": true,
  "data": {
    "range": "A1",
    "formula": "=SUM(B1:B10)"
  }
}
```

## Example
```bash
curl -X POST http://127.0.0.1:3000/set_formula \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "A1",
    "formula": "=SUM(B1:B10)"
  }'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Formula must start with =` | Formula does not start with `=` | Ensure formula starts with `=` |
| `#REF!` | Formula references a non-existent cell | Check that the referenced range is correct |
| `#NAME?` | Function name is misspelled or not supported | Confirm function name spelling and whether it is supported |
| `Sheet not found` | Worksheet name does not exist | Call get-sheet-list first to confirm the sheet name |
