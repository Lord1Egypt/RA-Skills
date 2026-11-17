---
name: oo-gleap
description: "Gleap (gleap.io). Use this skill for ANY Gleap request — reading, creating, updating, and deleting data. Whenever a task involves Gleap, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Gleap"
  author: "OOMOL"
  version: "1.0.4"
  services: ["gleap"]
  icon: "https://static.oomol.com/logo/third-party/gleap.svg"
---

# Gleap

Operate **Gleap** through your OOMOL-connected account. This skill calls the `gleap` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Gleap. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "gleap" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "gleap" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_contact` — Create a Gleap contact session in the connected project. [write]
- `create_ticket` — Create a Gleap ticket with native ticket fields. [write]
- `create_ticket_with_message` — Create a Gleap ticket with an optional initial message. [write]
- `delete_ticket` — Delete a Gleap ticket by ID. [destructive]
- `get_contact_by_user_id` — Get a Gleap contact session by external user ID.
- `get_current_user` — Get the current Gleap user for the connected API key.
- `get_ticket` — Get a Gleap ticket by ID.
- `list_contacts` — List Gleap contact sessions for the connected project.
- `list_tickets` — List Gleap tickets with documented filters, sorting, and pagination.
- `update_contact` — Update a Gleap contact session by session ID. [write]
- `update_ticket` — Update a Gleap ticket by ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Gleap state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Gleap is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/gleap
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Gleap homepage: https://www.gleap.io
- API documentation: https://docs.gleap.io/documentation/server/api-overview
