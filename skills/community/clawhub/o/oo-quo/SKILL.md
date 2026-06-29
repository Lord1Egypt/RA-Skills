---
name: oo-quo
description: "Quo (OpenPhone) (quo.com). Use this skill for ANY Quo (OpenPhone) request — reading, creating, updating, and deleting data. Whenever a task involves Quo (OpenPhone), use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Quo (OpenPhone)"
  author: "OOMOL"
  version: "1.0.2"
  services: ["quo"]
  icon: "https://static.oomol.com/logo/third-party/quo.svg"
---

# Quo (OpenPhone)

Operate **Quo (OpenPhone)** through your OOMOL-connected account. This skill calls the `quo` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Quo (OpenPhone). **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "quo" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "quo" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_contact` — Create a contact in the connected Quo workspace. [write]
- `delete_contact` — Delete a contact from the connected Quo workspace. [destructive]
- `get_contact` — Get details for a Quo contact by ID.
- `get_message` — Get details for a Quo message by ID.
- `get_phone_number` — Get details for a Quo phone number by ID.
- `get_user` — Get details for a Quo user by ID.
- `list_contacts` — List contacts in the connected Quo workspace with optional filters.
- `list_messages` — List messages exchanged between a Quo number and conversation participants.
- `list_phone_numbers` — List phone numbers in the connected Quo workspace.
- `list_users` — List users in the connected Quo workspace.
- `send_text_message` — Send a text message from a Quo phone number. [write]
- `update_contact` — Update a contact in the connected Quo workspace. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Quo (OpenPhone) state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Quo (OpenPhone) is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=quo
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Quo (OpenPhone) homepage: https://www.quo.com
