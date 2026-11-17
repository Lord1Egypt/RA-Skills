---
name: oo-softr
description: "Softr (softr.io). Use this skill for ANY Softr request — reading, creating, updating, and deleting data. Whenever a task involves Softr, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Softr"
  author: "OOMOL"
  version: "1.0.4"
  services: ["softr"]
  icon: "https://static.oomol.com/logo/third-party/softr.svg"
---

# Softr

Operate **Softr** through your OOMOL-connected account. This skill calls the `softr` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Softr. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "softr" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "softr" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_record` — Create one record in a Softr table. [write]
- `delete_record` — Permanently delete one Softr table record by ID. [destructive]
- `get_database` — Get one Softr database by ID.
- `get_record` — Get one Softr table record by ID.
- `get_table` — Get one Softr table and its field definitions by database ID and table ID.
- `get_table_field` — Get one Softr table field definition by ID.
- `list_databases` — List the Softr databases accessible to the connected Personal Access Token.
- `list_records` — List a paginated page of records from one Softr table, optionally filtered by a table view.
- `list_table_views` — List the configured views for one Softr table.
- `list_tables` — List all tables in a Softr database, including their field definitions.
- `search_records` — Search records in one Softr table using optional filters, sorting, and pagination.
- `update_record` — Partially update the supplied fields of one Softr table record. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Softr state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Softr is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/softr
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Softr homepage: https://www.softr.io/
- API documentation: https://docs.softr.io/softr-api/softr-database-api
