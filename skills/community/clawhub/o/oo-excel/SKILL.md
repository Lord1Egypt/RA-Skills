---
name: oo-excel
description: "Excel (microsoft.com). Use this skill for ANY Excel request — reading, creating, updating, and deleting data. Whenever a task involves Excel, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Excel"
  author: "OOMOL"
  version: "1.0.1"
  services: ["excel"]
  icon: "https://static.oomol.com/logo/third-party/excel.svg"
---

# Excel

Operate **Excel** through your OOMOL-connected account. This skill calls the `excel` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Excel. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "excel" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "excel" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_table` — Create a new workbook table from an address range. [write]
- `add_table_column` — Add one column to a workbook table. [write]
- `add_table_row` — Add one or more rows to a workbook table. [write]
- `add_worksheet` — Add a new worksheet to a workbook. [write]
- `apply_table_filter` — Apply a Microsoft Graph filter criteria object to one table column. [write]
- `apply_table_sort` — Apply a Microsoft Graph sort definition to one workbook table. [write]
- `clear_range` — Clear one worksheet range. [destructive]
- `clear_table_filter` — Clear the current Microsoft Graph filter on one table column. [destructive]
- `convert_table_to_range` — Convert a workbook table back into a plain worksheet range. [write]
- `create_session` — Create an Excel workbook session for subsequent workbook operations. [write]
- `create_workbook` — Create a new .xlsx workbook file and optionally populate worksheets and data. [write]
- `delete_table_column` — Delete one column from a workbook table. [destructive]
- `delete_table_row` — Delete one row from a workbook table by row index. [destructive]
- `delete_worksheet` — Delete one worksheet from a workbook. [destructive]
- `get_range` — Read one worksheet range by A1-style address.
- `get_table_column` — Read one workbook table column by column name or column ID.
- `get_workbook` — Read workbook metadata and optionally expand related workbook resources.
- `get_worksheet` — Read a single worksheet by worksheet name or worksheet ID.
- `get_worksheet_used_range` — Read the used range for one worksheet.
- `insert_range` — Insert one worksheet range and shift existing cells to make space. [write]
- `list_drive_item_children` — List direct child drive items for a folder or the drive root.
- `list_table_columns` — List columns for one workbook table.
- `list_table_rows` — List rows for one workbook table.
- `list_tables` — List workbook tables, optionally restricted to one worksheet.
- `list_worksheets` — List worksheets in a workbook.
- `merge_cells` — Merge cells inside one worksheet range. [write]
- `search_files` — Search workbook files in the current OneDrive drive and return matching drive items.
- `sort_range` — Apply a Microsoft Graph sort definition to one worksheet range. [write]
- `update_range` — Update one worksheet range with values, formulas, formats, or visibility flags. [write]
- `update_table` — Update table metadata such as the name, style, or header flags. [write]
- `update_worksheet` — Update worksheet metadata such as the name, position, or visibility. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Excel state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Excel is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=excel
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Excel homepage: https://www.microsoft.com/microsoft-365/excel
