---
name: oo-sendcloud
description: "SendCloud (sendcloud.net). Use this skill for ANY SendCloud request — reading, creating, updating, and deleting data. Whenever a task involves SendCloud, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SendCloud"
  author: "OOMOL"
  version: "1.0.0"
  services: ["sendcloud"]
  icon: "https://static.oomol.com/logo/third-party/sendcloud.svg"
---

# SendCloud

Operate **SendCloud** through your OOMOL-connected account. This skill calls the `sendcloud` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SendCloud. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sendcloud" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sendcloud" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_template` — Create a triggered or bulk SendCloud email template. [write]
- `delete_templates` — Delete SendCloud templates by invocation name or inclusive update-date range. When both are supplied, invocation name takes precedence. [destructive]
- `get_account` — Read the SendCloud account profile, balance and daily quota.
- `get_template` — Read a SendCloud template by its invocation name.
- `list_templates` — List SendCloud templates with optional name and type filters and offset pagination.
- `send_email` — Submit an HTML or plain-text email through SendCloud, with broadcast, individual or mailing-list recipients and optional hosted attachments. No automatic retries. [write]
- `send_template_email` — Submit email using a SendCloud template compatible with the connected API_USER type. Use xsmtpapi for individual recipients or to for existing mailing lists or broadcasts. No automatic retries. [write]
- `update_template` — Update a SendCloud template's display name, HTML, subject or type. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SendCloud state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SendCloud is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/sendcloud
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- SendCloud homepage: https://www.sendcloud.net/
- API documentation: https://www.sendcloud.net/doc/email_v2/
