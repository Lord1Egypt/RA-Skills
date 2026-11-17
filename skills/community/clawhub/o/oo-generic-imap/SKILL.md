---
name: oo-generic-imap
description: "IMAP Mailbox (rfc-editor.org). Use this skill for ANY IMAP Mailbox request — reading, creating, updating, and deleting data. Whenever a task involves IMAP Mailbox, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "IMAP Mailbox"
  author: "OOMOL"
  version: "1.0.5"
  services: ["generic_imap"]
  icon: "https://static.oomol.com/logo/third-party/generic_imap.svg"
---

# IMAP Mailbox

Operate **IMAP Mailbox** through your OOMOL-connected account. This skill calls the `generic_imap` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected IMAP Mailbox. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "generic_imap" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "generic_imap" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `delete_email` — Delete one IMAP Mailbox message from a folder. [destructive]
- `download_attachment` — Download one IMAP Mailbox attachment by IMAP body part identifier.
- `forward_email` — Forward one IMAP Mailbox email using SMTP with quoted original content. [write]
- `get_email` — Fetch and parse one IMAP Mailbox message without marking it as read.
- `get_folder_status` — Get lightweight message counters for one IMAP Mailbox folder.
- `list_folders` — List folders visible to the connected IMAP Mailbox account.
- `mark_email_read` — Mark one IMAP Mailbox message as read. [write]
- `mark_email_unread` — Mark one IMAP Mailbox message as unread. [write]
- `move_email` — Move one IMAP Mailbox message to another folder. [destructive]
- `reply_email` — Reply to one IMAP Mailbox email using SMTP reply headers and quoted content. [write]
- `search_emails` — Search one IMAP Mailbox folder and return lightweight email summaries.
- `send_email` — Send an email through IMAP Mailbox SMTP. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change IMAP Mailbox state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — IMAP Mailbox is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/generic_imap
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- IMAP Mailbox homepage: https://www.rfc-editor.org/rfc/rfc3501
- API documentation: https://www.rfc-editor.org/rfc/rfc3501
