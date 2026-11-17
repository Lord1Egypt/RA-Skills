---
name: oo-respond-io
description: "Respond.io (respond.io). Use this skill for ANY Respond.io request — reading, creating, updating, and deleting data. Whenever a task involves Respond.io, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Respond.io"
  author: "OOMOL"
  version: "1.0.5"
  services: ["respond_io"]
  icon: "https://static.oomol.com/logo/third-party/respond_io.svg"
---

# Respond.io

Operate **Respond.io** through your OOMOL-connected account. This skill calls the `respond_io` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Respond.io. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "respond_io" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "respond_io" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_contact_tags` — Add up to ten tags to a Respond.io contact. [write]
- `assign_conversation` — Assign or unassign the open conversation for a Respond.io contact. [destructive]
- `create_comment` — Add an internal comment to a Respond.io contact conversation. [write]
- `create_contact` — Create a Respond.io contact identified by an email address or phone number. [write]
- `create_or_update_contact` — Create a Respond.io contact when it does not exist, or update it when the identifier already exists. [write]
- `delete_contact` — Delete a Respond.io contact by contact ID, email address, or phone number. [destructive]
- `get_contact` — Get one Respond.io contact by contact ID, email address, or phone number.
- `list_channels` — List channels in the connected Respond.io workspace with cursor pagination.
- `list_contacts` — List Respond.io contacts using workspace timezone-aware filters and cursor pagination.
- `list_users` — List users in the connected Respond.io workspace with cursor pagination.
- `remove_contact_tags` — Remove up to ten tags from a Respond.io contact. [destructive]
- `update_contact` — Update one or more fields on an existing Respond.io contact. [write]
- `update_conversation_status` — Open or close a Respond.io contact conversation with optional closing context. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Respond.io state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Respond.io is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/respond_io
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Respond.io homepage: https://respond.io/
- API documentation: https://developers.respond.io/
