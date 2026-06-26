---
name: oo-airtable
description: "Airtable (airtable.com). Use this skill for ANY Airtable request — reading, creating, updating, and deleting data. Whenever a task involves Airtable, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Airtable"
  author: "OOMOL"
  version: "1.0.2"
  services: ["airtable"]
  icon: "https://static.oomol.com/logo/third-party/Airtable.svg"
---

# Airtable

Operate **Airtable** through your OOMOL-connected account. This skill calls the `airtable` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Airtable. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "airtable" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "airtable" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_base` — Create an Airtable base in a workspace with the provided initial table and field schema. [write]
- `create_field` — Create a field in an Airtable table. [write]
- `create_records` — Create one or more Airtable records in a table. [write]
- `create_table` — Create a table in an Airtable base with the provided field schema. [write]
- `delete_base` — Delete an Airtable base. Airtable restricts this endpoint to enterprise admins. [destructive]
- `delete_records` — Delete one or more Airtable records by record ID. [destructive]
- `get_base_collaborators` — Read Airtable base metadata, including workspaceId and optional collaborator details.
- `get_base_schema` — Read Airtable table, field, and view schema for a specific base.
- `get_record` — Read a single Airtable record by record ID.
- `list_bases` — List Airtable bases accessible to the authenticated personal access token.
- `list_records` — List Airtable records from a table with optional fields, sorting, view filters, formula filters, and pagination.
- `update_field` — Update an Airtable field name, description, or type-specific options. [write]
- `update_records` — Update one or more existing Airtable records by record ID. [write]
- `update_table` — Update an Airtable table name, description, or date dependency settings. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Airtable state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Airtable is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=airtable
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Airtable homepage: https://airtable.com
