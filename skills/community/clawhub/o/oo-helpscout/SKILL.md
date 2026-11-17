---
name: oo-helpscout
description: "Help Scout (helpscout.com). Use this skill for ANY Help Scout request — reading, creating, updating, and deleting data. Whenever a task involves Help Scout, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Help Scout"
  author: "OOMOL"
  version: "1.0.5"
  services: ["helpscout"]
  icon: "https://static.oomol.com/logo/third-party/helpscout.svg"
---

# Help Scout

Operate **Help Scout** through your OOMOL-connected account. This skill calls the `helpscout` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Help Scout. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "helpscout" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "helpscout" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `assign_conversation` — Assign a Help Scout conversation to a user or leave it unassigned. [destructive]
- `create_conversation` — Create a Help Scout conversation with one initial text thread. [write]
- `create_customer` — Create a Help Scout customer with a primary email address. [write]
- `create_note` — Add an internal note to a Help Scout conversation. [write]
- `create_reply` — Add a published reply or draft reply to a Help Scout conversation. [write]
- `get_conversation` — Get one Help Scout conversation by ID.
- `get_customer` — Get one Help Scout customer by ID.
- `get_saved_reply` — Get the complete email and chat content of a Help Scout saved reply.
- `list_conversations` — List and filter conversations in the connected Help Scout account.
- `list_customers` — List and filter customers in the connected Help Scout account.
- `list_inbox_custom_fields` — List the custom field definitions and dropdown options for a Help Scout inbox.
- `list_inbox_folders` — List the folders and conversation counts in a Help Scout inbox.
- `list_inboxes` — List the Help Scout inboxes available to the connected user.
- `list_saved_replies` — List the approved saved reply templates available in a Help Scout inbox.
- `list_tags` — List tags used across the connected Help Scout account.
- `list_threads` — List the complete threads belonging to a Help Scout conversation.
- `list_users` — List Help Scout users, optionally filtered by email or inbox.
- `list_workflows` — List Help Scout workflows, including the manual automations that can be run.
- `replace_conversation_custom_fields` — Replace the complete custom field state of a Help Scout conversation. [destructive]
- `replace_conversation_tags` — Replace the complete tag list on a Help Scout conversation. [destructive]
- `run_manual_workflow` — Run a configured Help Scout manual workflow on up to 50 conversations. [destructive]
- `set_conversation_status` — Replace the status of a Help Scout conversation. [destructive]
- `snooze_conversation` — Snooze a Help Scout conversation until a specific future time. [destructive]
- `unsnooze_conversation` — Remove the snooze from a Help Scout conversation and return it to its queue. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Help Scout state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Help Scout is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/helpscout
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Help Scout homepage: https://www.helpscout.com
- API documentation: https://developer.helpscout.com/mailbox-api/
