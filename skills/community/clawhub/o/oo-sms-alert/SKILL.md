---
name: oo-sms-alert
description: "SMS Alert (smsalert.co.in). Use this skill for ANY SMS Alert request — reading, creating, and updating data. Whenever a task involves SMS Alert, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SMS Alert"
  author: "OOMOL"
  version: "1.0.1"
  services: ["sms_alert"]
  icon: "https://static.oomol.com/logo/third-party/sms_alert.jpg"
---

# SMS Alert

Operate **SMS Alert** through your OOMOL-connected account. This skill calls the `sms_alert` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SMS Alert. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sms_alert" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sms_alert" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `generate_otp` — Generate and send an OTP message through SMS Alert.
- `get_credit_balance` — Get the remaining SMS Alert credits grouped by delivery route.
- `list_sender_ids` — List the sender IDs available in the SMS Alert account.
- `list_templates` — List SMS templates from the SMS Alert account with optional pagination.
- `send_sms` — Send a direct SMS message through SMS Alert. [write]
- `validate_otp` — Validate an OTP code previously generated through SMS Alert.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SMS Alert state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SMS Alert is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=sms_alert
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- SMS Alert homepage: https://www.smsalert.co.in/
