---
name: oo-resend
description: "Resend (resend.com). Use this skill for ANY Resend request — reading, creating, updating, and deleting data. Whenever a task involves Resend, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Resend"
  author: "OOMOL"
  version: "1.0.7"
  services: ["resend"]
  icon: "https://static.oomol.com/logo/third-party/Resend.svg"
---

# Resend

Operate **Resend** through your OOMOL-connected account. This skill calls the `resend` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Resend. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "resend" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "resend" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_scheduled_email` — Cancel a scheduled Resend email before delivery. [destructive]
- `get_received_email` — Retrieve one received Resend email, including its content, headers, and attachment metadata.
- `get_received_email_attachment` — Retrieve one attachment from a received Resend email, including its temporary download URL.
- `get_sent_email` — Retrieve one sent Resend email, including its message content and delivery state.
- `get_sent_email_attachment` — Retrieve one attachment from a sent Resend email, including its temporary download URL.
- `list_received_email_attachments` — List attachments for a received Resend email.
- `list_received_emails` — List emails received by the authenticated Resend team.
- `list_sent_email_attachments` — List attachments for a sent Resend email.
- `list_sent_emails` — List emails sent by the authenticated Resend team.
- `send_batch_emails` — Send up to 100 emails in one Resend batch request. [write]
- `send_email` — Send an email with Resend. [write]
- `update_scheduled_email` — Change the delivery time of a scheduled Resend email. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Resend state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Resend is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/resend
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Resend homepage: https://resend.com
- API documentation: https://resend.com/docs/api-reference/introduction
