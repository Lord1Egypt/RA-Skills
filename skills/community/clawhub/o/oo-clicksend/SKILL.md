---
name: oo-clicksend
description: "ClickSend (clicksend.com). Use this skill for ANY ClickSend request — reading, creating, updating, and deleting data. Whenever a task involves ClickSend, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "ClickSend"
  author: "OOMOL"
  version: "1.0.1"
  services: ["clicksend"]
  icon: "https://static.oomol.com/logo/third-party/clicksend.png"
---

# ClickSend

Operate **ClickSend** through your OOMOL-connected account. This skill calls the `clicksend` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected ClickSend. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "clicksend" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "clicksend" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `calculate_sms_price` — Calculate the ClickSend price for one or more SMS messages without sending them.
- `create_contact` — Create a contact in a ClickSend contact list. [write]
- `create_contact_list` — Create a ClickSend contact list. [write]
- `delete_contact` — Delete a ClickSend contact by list ID and contact ID. [destructive]
- `delete_contact_list` — Delete a ClickSend contact list by ID. [destructive]
- `get_account` — Get the ClickSend account profile associated with the configured credentials.
- `get_contact` — Get one ClickSend contact by list ID and contact ID.
- `get_contact_list` — Get one ClickSend contact list by ID.
- `list_contact_lists` — List ClickSend contact lists with pagination controls.
- `list_contacts` — List contacts in a ClickSend contact list.
- `send_sms` — Send one or more SMS messages through ClickSend. [write]
- `update_contact` — Update a ClickSend contact by list ID and contact ID. [write]
- `update_contact_list` — Update a ClickSend contact list name. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change ClickSend state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — ClickSend is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=clicksend
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- ClickSend homepage: https://www.clicksend.com/
