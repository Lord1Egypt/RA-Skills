---
name: oo-amplemarket
description: "Amplemarket (amplemarket.com). Use this skill for ANY Amplemarket request — reading, creating, and updating data. Whenever a task involves Amplemarket, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Amplemarket"
  author: "OOMOL"
  version: "1.0.5"
  services: ["amplemarket"]
  icon: "https://static.oomol.com/logo/third-party/amplemarket.svg"
---

# Amplemarket

Operate **Amplemarket** through your OOMOL-connected account. This skill calls the `amplemarket` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Amplemarket. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "amplemarket" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "amplemarket" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `complete_task` — Mark an Amplemarket task as completed. [write]
- `get_account_details` — Get account details for the authenticated Amplemarket API key.
- `get_contact` — Retrieve an Amplemarket contact by contact ID.
- `get_contact_by_email` — Retrieve an Amplemarket contact by email address.
- `get_lead_list` — Retrieve an Amplemarket lead list by ID.
- `list_contacts` — Retrieve Amplemarket contacts by one or more contact IDs.
- `list_lead_lists` — List Amplemarket lead lists with cursor pagination and owner filters.
- `list_task_statuses` — List task statuses supported by Amplemarket.
- `list_task_types` — List task types supported by Amplemarket.
- `list_tasks` — List Amplemarket tasks with cursor pagination and status, type, or user filters.
- `skip_task` — Skip an Amplemarket task. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Amplemarket state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Amplemarket is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/amplemarket
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Amplemarket homepage: https://www.amplemarket.com
- API documentation: https://docs.amplemarket.com/api-reference/introduction
