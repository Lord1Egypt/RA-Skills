---
name: oo-intercom
description: "Intercom (intercom.com). Use this skill for ANY Intercom request — reading, creating, and updating data. Whenever a task involves Intercom, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Intercom"
  author: "OOMOL"
  version: "1.0.1"
  services: ["intercom"]
  icon: "https://static.oomol.com/logo/third-party/Intercom.svg"
---

# Intercom

Operate **Intercom** through your OOMOL-connected account. This skill calls the `intercom` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Intercom. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "intercom" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "intercom" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `close_conversation` — Close an Intercom conversation. [write]
- `create_contact` — Create a new Intercom contact. [write]
- `get_admin` — Get a single Intercom admin by identifier.
- `get_contact` — Get a single Intercom contact by identifier.
- `get_contact_by_external_id` — Get a single Intercom contact by external ID.
- `get_conversation` — Get a single Intercom conversation with its conversation parts.
- `get_current_admin` — Get the currently authorized Intercom admin and workspace metadata.
- `list_admins` — List Intercom admins for the current workspace.
- `list_contacts` — List Intercom contacts with cursor-based pagination.
- `list_conversations` — List Intercom conversations with cursor-based pagination.
- `reopen_conversation` — Reopen an Intercom conversation. [write]
- `reply_to_conversation` — Reply to an Intercom conversation as an admin. [write]
- `search_contacts` — Search Intercom contacts with the official search DSL.
- `update_contact` — Update an existing Intercom contact. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Intercom state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Intercom is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=intercom
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Intercom homepage: https://www.intercom.com
