---
name: obsidian-sheet-plus-clear-all-conditional-formatting
description: Use when removing all conditional formatting rules from a sheet at once — for complete formatting reset
---

# clear-all-conditional-formatting
Clears all conditional formatting rules from the specified sheet. Removes all ranges and rule types at once.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/clear_all_conditional_formatting` |
| Auth | None by default. When enabled, requires `X-API-KEY` header |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active sheet | Target sheet name |

## Response
```json
{
  "success": true,
  "data": {
    "sheetName": "Sheet1"
  }
}
```

## Example
```bash
curl -X POST http://127.0.0.1:3000/clear_all_conditional_formatting \
  -H "Content-Type: application/json" \
  -d '{"sheetName": "Sheet1"}'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Sheet not found` | Sheet name does not exist | Call get-sheet-list first to confirm the sheet name |

## Related Tools
- **remove-conditional-formatting**: Remove conditional formatting from a specific range (not all)
- **add-conditional-formatting**: Add new conditional formatting rules
