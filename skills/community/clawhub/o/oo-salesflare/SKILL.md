---
name: oo-salesflare
description: "Salesflare (salesflare.com). Use this skill for ANY Salesflare request — reading, creating, and updating data. Whenever a task involves Salesflare, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Salesflare"
  author: "OOMOL"
  version: "1.0.0"
  services: ["salesflare"]
  icon: "https://static.oomol.com/logo/third-party/salesflare.svg"
---

# Salesflare

Operate **Salesflare** through your OOMOL-connected account. This skill calls the `salesflare` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Salesflare. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "salesflare" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "salesflare" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_account` — Create a Salesflare account. [write]
- `create_contact` — Create a Salesflare contact. [write]
- `create_opportunity` — Create a Salesflare opportunity. [write]
- `create_task` — Create a Salesflare task. [write]
- `get_account` — Retrieve one Salesflare account by ID.
- `get_contact` — Retrieve one Salesflare contact by ID.
- `get_current_user` — Retrieve the current Salesflare API user.
- `get_opportunity` — Retrieve one Salesflare opportunity by ID.
- `list_accounts` — List Salesflare accounts with optional search, pagination, and filters.
- `list_contacts` — List Salesflare contacts with optional search, pagination, and filters.
- `list_opportunities` — List Salesflare opportunities with optional search, pagination, and filters.
- `list_tasks` — List Salesflare tasks with optional search, pagination, and filters.
- `update_account` — Update a Salesflare account by ID. [write]
- `update_contact` — Update a Salesflare contact by ID. [write]
- `update_opportunity` — Update a Salesflare opportunity by ID. [write]
- `update_task` — Update a Salesflare task by ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Salesflare state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Salesflare is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=salesflare
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Salesflare homepage: https://salesflare.com
