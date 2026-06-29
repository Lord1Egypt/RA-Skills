---
name: oo-databar-ai
description: "Databar.ai (databar.ai). Use this skill for ANY Databar.ai request — reading, creating, and updating data. Whenever a task involves Databar.ai, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Databar.ai"
  author: "OOMOL"
  version: "1.0.0"
  services: ["databar_ai"]
  icon: "https://static.oomol.com/logo/third-party/databar_ai.svg"
---

# Databar.ai

Operate **Databar.ai** through your OOMOL-connected account. This skill calls the `databar_ai` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Databar.ai. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "databar_ai" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "databar_ai" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_table` — Create a Databar table with optional columns and empty rows. [write]
- `get_enrichment` — Get detailed Databar enrichment metadata by ID.
- `get_table_columns` — List columns for a Databar table.
- `get_table_rows` — Get Databar table rows with pagination and optional column filters.
- `get_task_status` — Get the status and result data for a Databar enrichment or waterfall task.
- `get_user_info` — Get the current Databar account information for the API key.
- `insert_rows` — Insert up to 50 rows into a Databar table using human-readable column names. [write]
- `list_enrichments` — List Databar enrichments with optional search and pagination.
- `list_tables` — List Databar tables in the current workspace.
- `run_enrichment` — Submit a Databar enrichment task and return the task ID for later status polling.
- `run_waterfall` — Submit a Databar waterfall task and return the task ID for later status polling.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Databar.ai state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Databar.ai is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=databar_ai
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Databar.ai homepage: https://databar.ai/
