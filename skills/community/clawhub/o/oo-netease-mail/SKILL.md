---
name: oo-netease-mail
description: "NetEase Mail (mail.163.com). Use this skill for ANY NetEase Mail request — reading, creating, updating, and deleting data. Whenever a task involves NetEase Mail, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "NetEase Mail"
  author: "OOMOL"
  version: "1.0.5"
  services: ["netease_mail"]
  icon: "https://static.oomol.com/logo/third-party/netease_mail.png"
---

# NetEase Mail

Operate **NetEase Mail** through your OOMOL-connected account. This skill calls the `netease_mail` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected NetEase Mail. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "netease_mail" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "netease_mail" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `delete_email` — Delete one NetEase Mail message from a folder. [destructive]
- `download_attachment` — Download one NetEase Mail attachment by IMAP body part identifier.
- `forward_email` — Forward one NetEase Mail email using SMTP with quoted original content. [write]
- `get_email` — Fetch and parse one NetEase Mail message without marking it as read.
- `get_folder_status` — Get lightweight message counters for one NetEase Mail folder.
- `list_folders` — List folders visible to the connected NetEase Mail account.
- `mark_email_read` — Mark one NetEase Mail message as read. [write]
- `mark_email_unread` — Mark one NetEase Mail message as unread. [write]
- `move_email` — Move one NetEase Mail message to another folder. [destructive]
- `reply_email` — Reply to one NetEase Mail email using SMTP reply headers and quoted content. [write]
- `search_emails` — Search one NetEase Mail folder and return lightweight email summaries.
- `send_email` — Send an email through NetEase Mail SMTP. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change NetEase Mail state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — NetEase Mail is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/netease_mail
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- NetEase Mail homepage: https://mail.163.com/
