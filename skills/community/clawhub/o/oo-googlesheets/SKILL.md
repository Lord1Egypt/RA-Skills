---
name: oo-googlesheets
description: "Google Sheets (workspace.google.com). Use this skill for ANY Google Sheets request — reading, creating, updating, and deleting data. Whenever a task involves Google Sheets, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Google Sheets"
  author: "OOMOL"
  version: "1.0.1"
  services: ["googlesheets"]
  icon: "https://static.oomol.com/logo/third-party/Google%20Sheets.svg"
---

# Google Sheets

Operate **Google Sheets** through your OOMOL-connected account. This skill calls the `googlesheets` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Google Sheets. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "googlesheets" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "googlesheets" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_sheet` — Add a new sheet through spreadsheets.batchUpdate and return stable batch replies. [write]
- `aggregate_column_data` — Aggregate numeric values from a target column, optionally filtered by another column, with stable counters.
- `append_dimension` — Append rows or columns through spreadsheets.batchUpdate and return stable batch replies. [write]
- `auto_resize_dimensions` — Auto-resize rows or columns through spreadsheets.batchUpdate and return stable batch replies. [write]
- `batch_clear_values_by_data_filter` — Clear spreadsheet values through values.batchClearByDataFilter and return the cleared ranges. [destructive]
- `batch_get` — Read multiple spreadsheet ranges through values:batchGet and return stable valueRanges output.
- `batch_update_values_by_data_filter` — Write spreadsheet values through values.batchUpdateByDataFilter and return stable aggregate counters. [write]
- `clear_basic_filter` — Clear a basic filter through spreadsheets.batchUpdate and return stable batch replies. [destructive]
- `clear_values` — Clear a single spreadsheet value range through values.clear and return the cleared A1 range. [destructive]
- `create_chart` — Create a chart through spreadsheets.batchUpdate and return stable batch replies. [write]
- `create_google_sheet1` — Create a Google Sheets spreadsheet and return stable spreadsheet metadata for the new file. [write]
- `create_spreadsheet_column` — Insert an empty column into a sheet through spreadsheets.batchUpdate with stable top-level fields. [write]
- `create_spreadsheet_row` — Insert an empty row into a sheet through spreadsheets.batchUpdate with stable top-level fields. [write]
- `delete_dimension` — Delete rows or columns through spreadsheets.batchUpdate and return stable batch replies. [destructive]
- `delete_sheet` — Delete a sheet through spreadsheets.batchUpdate and return stable batch replies. [destructive]
- `find_replace` — Run find and replace through spreadsheets.batchUpdate and return stable batch replies. [write]
- `format_cell` — Format cells through spreadsheets.batchUpdate and return stable batch replies. [write]
- `get_conditional_format_rules` — Read spreadsheet conditional formatting rules and project them into a stable per-sheet structure.
- `get_data_validation_rules` — Read spreadsheet data validation rules from the minimum necessary sheet ranges and return flattened rule entries.
- `get_sheet_names` — List visible or all sheet names from a spreadsheet and include a stable name-to-sheetId map.
- `get_spreadsheet_by_data_filter` — Read spreadsheet metadata through spreadsheets.getByDataFilter and return the normalized spreadsheet payload.
- `get_spreadsheet_info` — Read spreadsheet metadata through spreadsheets.get with optional ranges and grid data flags.
- `insert_dimension` — Insert rows or columns through spreadsheets.batchUpdate and return stable batch replies. [write]
- `lookup_spreadsheet_row` — Find the first row where a cell exactly matches the query and return a stable found/rowData payload.
- `mutate_conditional_format_rules` — Mutate conditional format rules through spreadsheets.batchUpdate and return stable batch replies. [write]
- `search_developer_metadata` — Search spreadsheet developer metadata via developerMetadata:search and return matched entries only.
- `search_spreadsheets` — Search Google Sheets files in Drive with spreadsheet-only filters and normalized summary output.
- `set_basic_filter` — Set a basic filter through spreadsheets.batchUpdate and return stable batch replies. [write]
- `set_data_validation_rule` — Set or clear data validation through spreadsheets.batchUpdate and return stable batch replies. [write]
- `spreadsheets_sheets_copy_to` — Copy a sheet to another spreadsheet through sheets.copyTo and return a stable copiedSheet payload. [write]
- `spreadsheets_values_append` — Append values through values.append and flatten the nested updates payload into stable top-level fields. [write]
- `spreadsheets_values_batch_clear` — Clear multiple spreadsheet value ranges through values.batchClear and return cleared ranges only. [destructive]
- `spreadsheets_values_batch_get_by_data_filter` — Read spreadsheet values through values:batchGetByDataFilter and return matched value ranges with their filters.
- `update_dimension_properties` — Update row or column properties through spreadsheets.batchUpdate and return stable batch replies. [write]
- `update_sheet_properties` — Update a sheet's properties through spreadsheets.batchUpdate and return stable batch replies. [write]
- `update_spreadsheet_properties` — Update spreadsheet-level properties through spreadsheets.batchUpdate and return stable batch replies. [write]
- `update_values_batch` — Write multiple spreadsheet value ranges through values.batchUpdate and return stable aggregate counters. [write]
- `upsert_rows` — Upsert rows by key while preserving uncovered columns, adding missing headers when needed, and returning stable counters. [write]
- `values_get` — Read a single spreadsheet value range and return a stable ValueRange without a wrapper envelope.
- `values_update` — Write a single spreadsheet value range through values.update and return stable update counters. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Google Sheets state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Google Sheets is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=googlesheets
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Google Sheets homepage: https://workspace.google.com/products/sheets/
