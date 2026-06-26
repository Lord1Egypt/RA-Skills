---
name: google-sheets-spreadsheets
description: Google Sheets API integration with managed OAuth. Create spreadsheets, read and write cell values, manage sheets, append rows, create charts, and automate data operations. Use this skill when users want spreadsheet work done in Google Sheets.
---

# Google Sheets

![Google Sheets](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/google-sheets.svg)

Access Google Sheets via the Google Sheets API with managed OAuth authentication. Create spreadsheets, read and write cell values, manage sheets, append rows, create charts, and automate data operations.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-sheets-spreadsheets) for hosted connection flows and credentials so you do not need to configure Google Sheets API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Google Sheets |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Google Sheets |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  Google Sheets   │
│   (User Chat)   │     │   (OAuth)    │     │   (Sheets API)   │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Sheets    │                       │
         │                       │  4. Secure Token       │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  Google  │
   │  File    │           │ Auth     │           │  Sheets  │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Google Sheets again."

## Quick Start

```bash
# Search for spreadsheets
clawlink_call_tool --tool "googlesheets_search_spreadsheets" --params '{"query": "budget"}'

# Get spreadsheet info
clawlink_call_tool --tool "googlesheets_get_spreadsheet_info" --params '{"spreadsheet_id": "YOUR_SPREADSHEET_ID"}'

# Get sheet names
clawlink_call_tool --tool "googlesheets_get_sheet_names" --params '{"spreadsheet_id": "YOUR_SPREADSHEET_ID"}'
```

## Authentication

All Google Sheets tool calls are authenticated automatically by ClawLink using the user's connected Google account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Google Sheets API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=google-sheets and connect Google Sheets.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `google-sheets` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration google-sheets
```

**Response:** Returns the live tool catalog for Google Sheets.

### Reconnect

If Google Sheets tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=google-sheets
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration google-sheets`

## Security & Permissions

- Access is scoped to spreadsheets within the connected Google account's Drive.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete sheet, clear values, delete dimension) are marked as high-impact and must be confirmed.
- Batch operations affect multiple cells and should be previewed before execution.

## Tool Reference

### Spreadsheet Discovery

| Tool | Description | Mode |
|------|-------------|------|
| `googlesheets_search_spreadsheets` | Search for spreadsheets by name, content, or date | Read |
| `googlesheets_get_spreadsheet_info` | Get spreadsheet metadata (ID, title, sheet properties) | Read |
| `googlesheets_get_sheet_names` | List all worksheet names in a spreadsheet | Read |
| `googlesheets_get_spreadsheet_by_data_filter` | Get spreadsheet filtered by data filters | Read |

### Reading Data

| Tool | Description | Mode |
|------|-------------|------|
| `googlesheets_values_get` | Read values from a specific cell range | Read |
| `googlesheets_batch_get` | Retrieve data from multiple ranges in one call | Read |
| `googlesheets_lookup_spreadsheet_row` | Find a row by exact cell content match | Read |
| `googlesheets_aggregate_column_data` | Search rows by column value and perform math operations | Read |
| `googlesheets_spreadsheets_values_batch_get_by_data_filter` | Read ranges matching data filters | Read |

### Writing & Updating Data

| Tool | Description | Mode |
|------|-------------|------|
| `googlesheets_values_update` | Set values in a cell range | Write |
| `googlesheets_update_values_batch` | Update multiple ranges in one call | Write |
| `googlesheets_spreadsheets_values_append` | Append new rows to a table | Write |
| `googlesheets_batch_update_values_by_data_filter` | Update values matching data filters | Write |
| `googlesheets_find_replace` | Find and replace text across a spreadsheet | Write |
| `googlesheets_format_cell` | Apply text and background formatting to cells | Write |

### Clearing Data

| Tool | Description | Mode |
|------|-------------|------|
| `googlesheets_clear_values` | Clear cell content from a range (preserves formatting) | Write |
| `googlesheets_spreadsheets_values_batch_clear` | Clear multiple ranges at once | Write |
| `googlesheets_batch_clear_values_by_data_filter` | Clear ranges matching data filters | Write |
| `googlesheets_clear_basic_filter` | Remove the basic filter from a sheet | Write |

### Sheet Management

| Tool | Description | Mode |
|------|-------------|------|
| `googlesheets_add_sheet` | Add a new sheet (GRID, OBJECT, or DATA_SOURCE type) | Write |
| `googlesheets_delete_sheet` | Delete a sheet from a spreadsheet | Write |
| `googlesheets_update_sheet_properties` | Rename, reposition, or change tab color of a sheet | Write |
| `googlesheets_update_spreadsheet_properties` | Update spreadsheet-level properties (title, locale, timezone) | Write |

### Row & Column Operations

| Tool | Description | Mode |
|------|-------------|------|
| `googlesheets_create_spreadsheet_row` | Insert a new row at a specific index | Write |
| `googlesheets_create_spreadsheet_column` | Insert a new column in a spreadsheet | Write |
| `googlesheets_delete_dimension` | Delete rows or columns by range | Write |
| `googlesheets_insert_dimension` | Insert empty rows or columns at a location | Write |
| `googlesheets_append_dimension` | Append rows or columns to a sheet | Write |
| `googlesheets_update_dimension_properties` | Hide/unhide rows or columns, set row height/column width | Write |
| `googlesheets_auto_resize_dimensions` | Auto-fit column widths or row heights to content | Write |

### Smart Upsert

| Tool | Description | Mode |
|------|-------------|------|
| `googlesheets_upsert_rows` | Update existing rows by key column, append new ones if not found | Write |

### Charts

| Tool | Description | Mode |
|------|-------------|------|
| `googlesheets_create_chart` | Create a chart from a data range with configurable chart type | Write |

### Filtering & Validation

| Tool | Description | Mode |
|------|-------------|------|
| `googlesheets_set_basic_filter` | Set or update a basic filter on a sheet | Write |
| `googlesheets_set_data_validation_rule` | Apply data validation rules or dropdowns to a range | Write |
| `googlesheets_get_conditional_format_rules` | List conditional formatting rules for a sheet | Read |
| `googlesheets_mutate_conditional_format_rules` | Add, update, delete, or reorder conditional format rules | Write |
| `googlesheets_get_data_validation_rules` | Extract data validation rules from a spreadsheet | Read |

### Spreadsheet Creation

| Tool | Description | Mode |
|------|-------------|------|
| `googlesheets_create_google_sheet1` | Create a new spreadsheet, optionally in a specific Drive folder | Write |

### Copy & Transfer

| Tool | Description | Mode |
|------|-------------|------|
| `googlesheets_spreadsheets_sheets_copy_to` | Copy a single sheet to another spreadsheet | Write |

### Metadata

| Tool | Description | Mode |
|------|-------------|------|
| `googlesheets_search_developer_metadata` | Search for developer metadata in a spreadsheet | Read |

## Code Examples

### Search for spreadsheets

```bash
clawlink_call_tool --tool "googlesheets_search_spreadsheets" \
  --params '{
    "query": "budget tracker"
  }'
```

### Read a cell range

```bash
clawlink_call_tool --tool "googlesheets_values_get" \
  --params '{
    "spreadsheet_id": "YOUR_SPREADSHEET_ID",
    "range": "Sheet1!A1:C10"
  }'
```

### Update cell values

```bash
clawlink_call_tool --tool "googlesheets_values_update" \
  --params '{
    "spreadsheet_id": "YOUR_SPREADSHEET_ID",
    "range": "Sheet1!A1:B2",
    "values": [["Product", "Revenue"], ["Widget", 1500]]
  }'
```

### Append rows to a table

```bash
clawlink_call_tool --tool "googlesheets_spreadsheets_values_append" \
  --params '{
    "spreadsheet_id": "YOUR_SPREADSHEET_ID",
    "range": "Sheet1!A:C",
    "values": [["New Item", "Description", 100]]
  }'
```

### Upsert rows by key

```bash
clawlink_call_tool --tool "googlesheets_upsert_rows" \
  --params '{
    "spreadsheet_id": "YOUR_SPREADSHEET_ID",
    "sheet": "Sheet1",
    "key_column": "Email",
    "headers": ["Email", "Phone", "Status"],
    "data": [["john@example.com", "555-0101", "Active"]]
  }'
```

### Create a chart

```bash
clawlink_call_tool --tool "googlesheets_create_chart" \
  --params '{
    "spreadsheet_id": "YOUR_SPREADSHEET_ID",
    "sheet_id": 0,
    "chart_type": "BAR",
    "data_range": "A1:B5",
    "title": "Monthly Revenue"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Google Sheets is connected.
2. Call `clawlink_list_tools --integration google-sheets` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `google-sheets`.
5. If no Google Sheets tools appear, direct the user to https://claw-link.dev/dashboard?add=google-sheets.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  search → get → read → call                                 │
│                                                             │
│  Example: List sheets → Read range → Show results          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Describe tool → Preview changes → User approves    │
│           → Execute update                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer spreadsheet inspection and range reads before writes.
4. For updates, appends, clears, sheet creation or deletion, structural edits, formatting changes, or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Spreadsheet IDs are the long ID string in the spreadsheet URL.
- Sheet IDs can be numeric (for existing sheets) or referenced by name.
- Use `null` in value arrays to skip updating specific cells.
- Blank cells should use `""` (empty string).
- Range addresses use A1 notation (e.g., `Sheet1!A1:C10`).
- `upsert_rows` auto-adds missing columns and performs partial column updates.
- Sheet names must be unique within a spreadsheet.
- `find_replace` is useful for fixing formula errors or bulk text updates.
- Avoid creating sheets in parallel — the `index` field can cause conflicts.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration google-sheets`. |
| Missing connection | Google Sheets is not connected. Direct the user to https://claw-link.dev/dashboard?add=google-sheets. |
| `SPREADSHEET_NOT_FOUND` | Spreadsheet does not exist. Check the spreadsheet_id. |
| `INVALID_ARGUMENT` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `google-sheets`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Google Sheets API Overview](https://developers.google.com/sheets/api)
- [Values Resource](https://developers.google.com/sheets/api/reference/spreadsheets.values)
- [Spreadsheets Resource](https://developers.google.com/sheets/api/reference/spreadsheets)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-sheets-spreadsheets
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Microsoft Excel](https://clawhub.ai/hith3sh/microsoft-excel-spreadsheets) — For Excel workbook operations via Microsoft Graph
- [Google Drive](https://clawhub.ai/hith3sh/google-drive-files) — For file management and Drive-level operations

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-sheets-spreadsheets)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)