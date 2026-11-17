---
name: oo-mailsoftly
description: "Mailsoftly (mailsoftly.com). Use this skill for ANY Mailsoftly request — reading, creating, and updating data. Whenever a task involves Mailsoftly, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Mailsoftly"
  author: "OOMOL"
  version: "1.0.4"
  services: ["mailsoftly"]
  icon: "https://static.oomol.com/logo/third-party/mailsoftly.png"
---

# Mailsoftly

Operate **Mailsoftly** through your OOMOL-connected account. This skill calls the `mailsoftly` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Mailsoftly. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "mailsoftly" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "mailsoftly" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_contact_to_contact_list` — Add an existing Mailsoftly contact to a contact list. [write]
- `add_contacts_to_contact_list` — Add contacts to a Mailsoftly list by email, creating contacts that do not already exist. [write]
- `create_contact` — Create a Mailsoftly contact with a unique email address. [write]
- `create_contact_list` — Create an empty Mailsoftly contact list. [write]
- `get_contact` — Retrieve one Mailsoftly contact by ID, optionally with detailed fields.
- `get_contact_list` — Retrieve one Mailsoftly contact list by ID.
- `get_contact_list_contacts` — List contacts belonging to a Mailsoftly contact list.
- `get_contact_lists` — List general Mailsoftly contact lists and their contact counts.
- `get_contacts` — List all contacts in the authenticated Mailsoftly account.
- `search_contacts` — Search Mailsoftly contacts by exact email, first name, or last name.
- `update_contact` — Update selected fields on an existing Mailsoftly contact. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Mailsoftly state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Mailsoftly is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/mailsoftly
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Mailsoftly homepage: https://mailsoftly.com/
- API documentation: https://app.mailsoftly.com/developers
