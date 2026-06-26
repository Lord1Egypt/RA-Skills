---
name: oo-zendesk
description: "Zendesk (zendesk.com). Use this skill for ANY Zendesk request — reading, creating, and updating data. Whenever a task involves Zendesk, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Zendesk"
  author: "OOMOL"
  version: "1.0.1"
  services: ["zendesk"]
  icon: "https://static.oomol.com/logo/third-party/Zendesk.svg"
---

# Zendesk

Operate **Zendesk** through your OOMOL-connected account. This skill calls the `zendesk` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Zendesk. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "zendesk" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "zendesk" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_ticket` — Create a Zendesk ticket with an initial comment. [write]
- `get_current_user` — Get the current authenticated Zendesk user.
- `get_organization` — Get a Zendesk organization by identifier.
- `get_ticket` — Get a Zendesk ticket and its comments by identifier.
- `get_user` — Get a Zendesk user by identifier.
- `list_organizations` — List Zendesk organizations with pagination.
- `list_tickets` — List Zendesk tickets with offset or cursor pagination.
- `list_users` — List Zendesk users with optional role and pagination filters.
- `reply_to_ticket` — Append a public reply or internal note to a Zendesk ticket. [write]
- `search_users` — Search Zendesk users by email address or name.
- `update_ticket` — Update fields on an existing Zendesk ticket. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Zendesk state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Zendesk is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=zendesk
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Zendesk homepage: https://www.zendesk.com
