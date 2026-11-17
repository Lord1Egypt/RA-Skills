---
name: oo-sheetdb
description: "SheetDB (sheetdb.io). Use this skill for ANY SheetDB request — reading, creating, updating, and deleting data. Whenever a task involves SheetDB, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SheetDB"
  author: "OOMOL"
  version: "1.0.5"
  services: ["sheetdb"]
  icon: "https://static.oomol.com/logo/third-party/sheetdb.svg"
---

# SheetDB

Operate **SheetDB** through your OOMOL-connected account. This skill calls the `sheetdb` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SheetDB. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sheetdb" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sheetdb" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `count_rows` — Count data rows in the connected spreadsheet, excluding the header row.
- `create_rows` — Append one or more JSON rows to the connected spreadsheet. [write]
- `delete_rows` — Delete all rows matching one spreadsheet column and value. [destructive]
- `get_document_name` — Get the Google Sheets document name for the connected SheetDB API.
- `get_keys` — Get the column names from the first row of the connected spreadsheet.
- `list_rows` — List rows from the connected SheetDB spreadsheet with optional paging and sorting.
- `search_rows` — Search spreadsheet rows using dynamic column conditions and AND or OR matching.
- `update_rows` — Update all rows matching one spreadsheet column and value. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SheetDB state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SheetDB is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/sheetdb
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- SheetDB homepage: https://sheetdb.io
- API documentation: https://docs.sheetdb.io
