---
name: oo-smtp2go
description: "SMTP2GO (smtp2go.com). Use this skill for ANY SMTP2GO request — reading, creating, and updating data. Whenever a task involves SMTP2GO, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SMTP2GO"
  author: "OOMOL"
  version: "1.0.5"
  services: ["smtp2go"]
  icon: "https://static.oomol.com/logo/third-party/smtp2go.png"
---

# SMTP2GO

Operate **SMTP2GO** through your OOMOL-connected account. This skill calls the `smtp2go` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SMTP2GO. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "smtp2go" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "smtp2go" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_email_summary` — Retrieve SMTP2GO account email statistics and current sending cycle summary.
- `get_email_template` — Retrieve details for a single SMTP2GO email template by ID.
- `list_sender_domains` — List SMTP2GO sender domains and their verification metadata.
- `list_single_sender_emails` — List SMTP2GO single sender email addresses and verification status.
- `search_activity` — Search SMTP2GO email activity events with optional filters and pagination.
- `search_email_templates` — Search SMTP2GO email templates by terms, tags, sorting, and pagination.
- `send_email` — Send a standard JSON email through SMTP2GO without Base64 attachments or inline files. [write]
- `view_api_key_permissions` — List the SMTP2GO API endpoint permissions available to the connected API key.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SMTP2GO state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SMTP2GO is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/smtp2go
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- SMTP2GO homepage: https://www.smtp2go.com/
- API documentation: https://apidoc.smtp2go.com/
