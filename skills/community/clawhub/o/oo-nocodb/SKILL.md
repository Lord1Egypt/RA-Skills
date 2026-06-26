---
name: oo-nocodb
description: "NocoDB (nocodb.com). Use this skill for ANY NocoDB request — reading, creating, updating, and deleting data. Whenever a task involves NocoDB, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "NocoDB"
  author: "OOMOL"
  version: "1.0.2"
  services: ["nocodb"]
  icon: "https://static.oomol.com/logo/third-party/nocodb.svg"
---

# NocoDB

Operate **NocoDB** through your OOMOL-connected account. This skill calls the `nocodb` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected NocoDB. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "nocodb" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "nocodb" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `count_records` — Count records in one NocoDB table, optionally filtered by a where expression.
- `count_table_records` — Count records in one NocoDB table using the v3 data API.
- `create_records` — Create one or more records in a NocoDB table. [write]
- `create_table` — Create a table in a NocoDB base using the v3 metadata API. [write]
- `create_table_field` — Create a field in a NocoDB table using the v3 metadata API. [write]
- `create_table_records` — Create one or more records in a NocoDB table using the v3 data API. [write]
- `create_table_view` — Create a view for a NocoDB table using the v3 metadata API. [write]
- `delete_records` — Delete one or more records from a NocoDB table. [destructive]
- `delete_table` — Delete a NocoDB table using the v3 metadata API. [destructive]
- `delete_table_records` — Delete one or more records from a NocoDB table using the v3 data API. [destructive]
- `get_base_schema` — Get schema metadata for one NocoDB base.
- `get_current_user` — Get the NocoDB user associated with the connected API token.
- `get_table_metadata` — Get metadata for one NocoDB table, including columns and views when available.
- `list_bases` — List bases visible to the connected NocoDB API token.
- `list_records` — List records from one NocoDB table with optional where, sort, field, limit, and offset query parameters.
- `list_table_records` — List records from one NocoDB table using the v3 data API with optional field, sort, filter, page, and view parameters.
- `list_table_views` — List views for a NocoDB table using the v3 metadata API.
- `list_tables` — List tables in a NocoDB base or in a specific base source.
- `read_record` — Read one record from a NocoDB table by record ID.
- `read_table_record` — Read one record from a NocoDB table using the v3 data API.
- `update_records` — Update one or more records in a NocoDB table. [write]
- `update_table` — Update a NocoDB table title, description, display field, or metadata using the v3 metadata API. [write]
- `update_table_records` — Update one or more records in a NocoDB table using the v3 data API. [write]
- `upsert_table_records` — Create or update records in a NocoDB table by matching up to three fields using the v3 data API. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change NocoDB state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — NocoDB is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=nocodb
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- NocoDB homepage: https://nocodb.com
