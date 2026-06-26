---
name: oo-asin-data-api
description: "ASIN Data API (asindataapi.com). Use this skill for ANY ASIN Data API request — reading, creating, updating, and deleting data. Whenever a task involves ASIN Data API, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "ASIN Data API"
  author: "OOMOL"
  version: "1.0.1"
  services: ["asin_data_api"]
  icon: "https://static.oomol.com/logo/third-party/asin_data_api.png"
---

# ASIN Data API

Operate **ASIN Data API** through your OOMOL-connected account. This skill calls the `asin_data_api` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected ASIN Data API. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "asin_data_api" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "asin_data_api" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `clear_collection_requests` — Delete multiple requests from a collection by their request IDs in ASIN Data API. [destructive]
- `delete_destination` — Delete a destination from the ASIN Data API account. [destructive]
- `get_collection` — Get details of a specific ASIN Data API collection including status and request counts.
- `list_collection_requests` — List requests in an ASIN Data API collection by page.
- `list_destinations` — List destinations configured on the ASIN Data API account with optional filtering and sorting.
- `update_destination` — Update an existing ASIN Data API destination configuration. Only include fields you want to update. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change ASIN Data API state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — ASIN Data API is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=asin_data_api
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- ASIN Data API homepage: https://www.asindataapi.com
