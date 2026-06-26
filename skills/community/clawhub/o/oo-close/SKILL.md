---
name: oo-close
description: "Close (close.com). Use this skill for ANY Close request — reading, creating, and updating data. Whenever a task involves Close, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Close"
  author: "OOMOL"
  version: "1.0.1"
  services: ["close"]
  icon: "https://static.oomol.com/logo/third-party/Close.svg"
---

# Close

Operate **Close** through your OOMOL-connected account. This skill calls the `close` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Close. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "close" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "close" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_contact` — Create a Close contact under a specific lead. [write]
- `create_lead` — Create a Close lead with optional nested contacts and addresses. [write]
- `create_opportunity` — Create a Close opportunity for an existing lead. [write]
- `create_task` — Create a lead-scoped Close task. [write]
- `get_contact` — Fetch a single Close contact by ID.
- `get_lead` — Fetch a single Close lead by ID.
- `get_opportunity` — Fetch a single Close opportunity by ID.
- `get_task` — Fetch a single Close task by ID.
- `list_contacts` — List Close contacts with optional lead filtering and pagination.
- `list_leads` — List Close leads with optional pagination and field selection.
- `list_opportunities` — List Close opportunities with stable workflow filters and pagination.
- `list_tasks` — List Close tasks with lead, assignee, completion, and view filters.
- `update_contact` — Update writable fields on an existing Close contact. [write]
- `update_lead` — Update writable fields on an existing Close lead. [write]
- `update_opportunity` — Update writable fields on an existing Close opportunity. [write]
- `update_task` — Update writable fields on an existing Close task. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Close state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Close is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=close
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Close homepage: https://www.close.com
