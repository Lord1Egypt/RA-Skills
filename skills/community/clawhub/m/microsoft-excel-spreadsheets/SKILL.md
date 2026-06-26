---
name: microsoft-excel-spreadsheets
description: Microsoft Excel API integration with managed OAuth. Read and write Excel workbooks, worksheets, ranges, tables, and charts stored in OneDrive. Use this skill when users want to read or modify Excel spreadsheets, manage worksheet data, work with tables, or access cell values.
---

# Microsoft Excel

![Microsoft Excel](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/microsoft-excel.svg)

Access Microsoft Excel via the Microsoft Graph API with managed OAuth authentication. Read and write workbooks, worksheets, ranges, tables, and charts stored in OneDrive or SharePoint.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=microsoft-excel-spreadsheets) for hosted connection flows and credentials so you do not need to configure Microsoft Excel API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Excel |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | ![Connect](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/excel.gif) |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Microsoft Excel |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Microsoft Graph  │
│   (User Chat)   │     │   (OAuth)    │     │   (Excel API)    │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Excel     │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ OneDrive │
   │  File    │           │ Auth     │           │ Excel    │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Microsoft Excel again."

## Quick Start

```bash
# List worksheets in a workbook
clawlink_call_tool --tool "excel_list_worksheets" --params '{"file_id": "WORKBOOK_ID"}'

# Read a cell range
clawlink_call_tool --tool "excel_get_range" --params '{"file_id": "WORKBOOK_ID", "worksheet_name": "Sheet1", "range_address": "A1:B10"}'

# Update a cell range
clawlink_call_tool --tool "excel_update_range" --params '{"file_id": "WORKBOOK_ID", "worksheet_name": "Sheet1", "range_address": "A1:B2", "values": [["Name", "Age"], ["Alice", 30]]}'
```

## Authentication

All Microsoft Excel tool calls are authenticated automatically by ClawLink using the user's connected Microsoft account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Microsoft Graph request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=microsoft-excel and connect Microsoft Excel.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `microsoft-excel` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration microsoft-excel
```

**Response:** Returns the live tool catalog for Microsoft Excel.

### Reconnect

If Microsoft Excel tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=microsoft-excel
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration microsoft-excel`

## Workbook Access Patterns

You can access workbooks using either **OneDrive** or **SharePoint** paths:

**By File ID (OneDrive):**
```bash
clawlink_call_tool --tool "excel_get_workbook" --params '{"file_id": "YOUR_FILE_ID"}'
```

**By File Path (OneDrive):**
```bash
clawlink_call_tool --tool "excel_search_files" --params '{"query": "workbook.xlsx"}'
```

**SharePoint workbooks:**
Use the `sharepoint` variants of tools (e.g., `excel_get_sharepoint_worksheet`, `excel_update_sharepoint_range`).

## Security & Permissions

- Access is scoped to workbooks, worksheets, tables, and cell data within the connected Microsoft account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete worksheet, clear range, delete table row/column) are marked as high-impact and must be confirmed.
- Workbook permissions can be inspected with `excel_list_workbook_permissions` and granted with `excel_add_workbook_permission`.

## Tool Reference

### Drive & File Operations

| Tool | Description | Mode |
|------|-------------|------|
| `excel_search_files` | Search OneDrive for Excel workbook IDs by name or query | Read |
| `excel_list_files` | List files and folders in a drive root or path | Read |
| `excel_list_drive_item_children` | List immediate children of a folder with pagination | Read |
| `excel_create_workbook` | Create a new `.xlsx` file with worksheets and data in OneDrive | Write |
| `excel_upload_workbook` | Upload an external Excel file from a URL into OneDrive/SharePoint | Write |
| `excel_export_workbook_to_pdf` | Export an Excel workbook to PDF via Microsoft Graph | Write |

### Session Management

| Tool | Description | Mode |
|------|-------------|------|
| `excel_get_session` | Create a persistent workbook session for batch operations | Write |
| `excel_close_session` | Close an active workbook session to release locks | Write |

**Note:** Sessions expire after ~5 minutes of inactivity (persistent) or ~7 minutes (non-persistent). Pass the `session_id` in subsequent write operations when available.

### Worksheet Operations

| Tool | Description | Mode |
|------|-------------|------|
| `excel_list_worksheets` | List all worksheets in a workbook | Read |
| `excel_get_worksheet` | Get a worksheet by name or ID | Read |
| `excel_add_worksheet` | Add a new worksheet to a workbook | Write |
| `excel_update_worksheet` | Rename or reposition a worksheet | Write |
| `excel_delete_worksheet` | Delete a worksheet from the workbook | Write |
| `excel_protect_worksheet` | Protect a worksheet from editing | Write |
| `excel_get_worksheet_used_range` | Get the active data region of a worksheet | Read |

### Range Operations

| Tool | Description | Mode |
|------|-------------|------|
| `excel_get_range` | Read values, formulas, and formatting from a cell range | Read |
| `excel_update_range` | Update values and formatting in a cell range | Write |
| `excel_clear_range` | Clear contents, formats, or both from a range | Write |
| `excel_insert_range` | Insert cells, shifting existing content down or right | Write |
| `excel_sort_range` | Sort a range by one or more columns | Write |
| `excel_merge_cells` | Merge cells in a worksheet range | Write |

### Table Operations

| Tool | Description | Mode |
|------|-------------|------|
| `excel_list_tables` | List all tables in a worksheet | Read |
| `excel_get_table_column` | Get a specific table column by ID or name | Read |
| `excel_list_table_columns` | List all columns in a table | Read |
| `excel_list_table_rows` | List all rows in a table | Read |
| `excel_add_table` | Create a new table from a range | Write |
| `excel_update_table` | Update table properties (name, style, totals) | Write |
| `excel_add_table_row` | Append a row to a table | Write |
| `excel_add_table_column` | Append a column to a table | Write |
| `excel_delete_table_row` | Delete a row from a table by index | Write |
| `excel_delete_table_column` | Delete a column from a table by index | Write |
| `excel_apply_table_filter` | Apply a filter to a table column | Write |
| `excel_clear_table_filter` | Clear an existing filter from a table | Write |
| `excel_apply_table_sort` | Apply a sort to a table | Write |
| `excel_convert_table_to_range` | Convert a table back to a plain range | Write |

### Chart Operations

| Tool | Description | Mode |
|------|-------------|------|
| `excel_list_charts` | List all charts in a worksheet | Read |
| `excel_list_chart_series` | List data series in a chart | Read |
| `excel_get_chart_axis` | Retrieve axis properties (min, max, interval) | Read |
| `excel_get_chart_data_labels` | Retrieve chart data label settings | Read |
| `excel_get_chart_legend` | Retrieve chart legend visibility and formatting | Read |
| `excel_add_chart` | Add a new chart to a worksheet | Write |
| `excel_update_chart` | Update an existing chart | Write |
| `excel_update_chart_legend` | Update chart legend position or formatting | Write |

### SharePoint Operations

| Tool | Description | Mode |
|------|-------------|------|
| `excel_list_sharepoint_worksheets` | List worksheets in a SharePoint workbook | Read |
| `excel_get_sharepoint_worksheet` | Get a worksheet from a SharePoint workbook | Read |
| `excel_get_sharepoint_range` | Read a range from a SharePoint worksheet | Read |
| `excel_update_sharepoint_range` | Update a range in a SharePoint worksheet | Write |
| `excel_list_sharepoint_tables` | List tables in a SharePoint worksheet | Read |
| `excel_add_sharepoint_worksheet` | Add a worksheet to a SharePoint workbook | Write |

### Workbook Metadata

| Tool | Description | Mode |
|------|-------------|------|
| `excel_get_workbook` | Retrieve workbook properties, tables, and worksheets | Read |
| `excel_list_named_items` | List named ranges and items in a workbook | Read |
| `excel_list_comments` | List all comments in a workbook | Read |
| `excel_list_workbook_permissions` | List sharing permissions on a workbook file | Read |
| `excel_add_workbook_permission` | Grant access to a workbook via invite | Write |

## Code Examples

### Read a range

```bash
clawlink_call_tool --tool "excel_get_range" \
  --params '{
    "file_id": "YOUR_FILE_ID",
    "worksheet_name": "Sheet1",
    "range_address": "A1:C10"
  }'
```

### Update a range

```bash
clawlink_call_tool --tool "excel_update_range" \
  --params '{
    "file_id": "YOUR_FILE_ID",
    "worksheet_name": "Sheet1",
    "range_address": "A1:B2",
    "values": [["Updated", "Values"], [100, 200]]
  }'
```

### Create a table

```bash
clawlink_call_tool --tool "excel_add_table" \
  --params '{
    "file_id": "YOUR_FILE_ID",
    "worksheet_name": "Sheet1",
    "address": "A1:C4",
    "has_headers": true
  }'
```

### Add a table row

```bash
clawlink_call_tool --tool "excel_add_table_row" \
  --params '{
    "file_id": "YOUR_FILE_ID",
    "table_name": "Table1",
    "values": [["Carol", 35, "Chicago"]]
  }'
```

### Add a chart

```bash
clawlink_call_tool --tool "excel_add_chart" \
  --params '{
    "file_id": "YOUR_FILE_ID",
    "worksheet_name": "Sheet1",
    "type": "ColumnClustered",
    "source_data": "A1:C4",
    "series_by": "Auto"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Microsoft Excel is connected.
2. Call `clawlink_list_tools --integration microsoft-excel` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `microsoft-excel`.
5. If no Microsoft Excel tools appear, direct the user to https://claw-link.dev/dashboard?add=microsoft-excel.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List worksheets → Read range → Show results       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update                                  │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Only `.xlsx` files are supported (not legacy `.xls`).
- Worksheet names with special characters may need URL encoding when using direct Graph paths.
- Table and worksheet IDs containing `{` and `}` must be URL-encoded (`%7B` and `%7D`) in raw Graph URLs. ClawLink handles this automatically.
- Use `null` in value arrays to skip updating specific cells.
- Blank cells should use `""` (empty string).
- Range addresses use A1 notation (e.g., `A1:C10`, `Sheet1!A1:B5`).
- When piping shell output, environment variables may not expand correctly in some shells; prefer explicit JSON parameters.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration microsoft-excel`. |
| Missing connection | Microsoft Excel is not connected. Direct the user to https://claw-link.dev/dashboard?add=microsoft-excel. |
| `ItemNotFound` | File or resource does not exist. Check the `file_id` or path. |
| `ItemAlreadyExists` | Worksheet or table with that name already exists. |
| `InvalidArgument` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| `SessionNotFound` | Session expired or does not exist. Create a new session with `excel_get_session`. |
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

1. Ensure the integration slug is exactly `microsoft-excel`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Microsoft Graph Excel API Overview](https://learn.microsoft.com/en-us/graph/api/resources/excel)
- [Working with Excel in Microsoft Graph](https://learn.microsoft.com/en-us/graph/excel-concept-overview)
- [Excel Workbook Resource](https://learn.microsoft.com/en-us/graph/api/resources/workbook)
- [Excel Worksheet Resource](https://learn.microsoft.com/en-us/graph/api/resources/worksheet)
- [Excel Range Resource](https://learn.microsoft.com/en-us/graph/api/resources/range)
- [Excel Table Resource](https://learn.microsoft.com/en-us/graph/api/resources/table)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=microsoft-excel-spreadsheets
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Google Sheets](https://clawhub.ai/hith3sh/google-sheets-spreadsheets) — For Google Workspace spreadsheet operations
- [OneDrive](https://clawhub.ai/hith3sh/onedrive-files) — For general OneDrive file management
- [SharePoint](https://clawhub.ai/hith3sh/sharepoint-sites) — For SharePoint site and file operations

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=microsoft-excel-spreadsheets)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
