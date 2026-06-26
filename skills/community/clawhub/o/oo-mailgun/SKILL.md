---
name: oo-mailgun
description: "Mailgun (mailgun.com). Use this skill for ANY Mailgun request — reading, creating, updating, and deleting data. Whenever a task involves Mailgun, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Mailgun"
  author: "OOMOL"
  version: "1.0.1"
  services: ["mailgun"]
  icon: "https://static.oomol.com/logo/third-party/mailgun.svg"
---

# Mailgun

Operate **Mailgun** through your OOMOL-connected account. This skill calls the `mailgun` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Mailgun. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "mailgun" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "mailgun" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_suppression` — Add one Mailgun suppression or allowlist record. [write]
- `create_template` — Create a Mailgun template and optionally its initial active version. [write]
- `create_template_version` — Create a new version for a Mailgun template. [write]
- `delete_suppression` — Remove one Mailgun suppression or allowlist record. [destructive]
- `get_domain` — Get Mailgun domain details including DNS records and sending state.
- `get_domain_tracking_settings` — Get open, click, unsubscribe, and web scheme tracking settings for a domain.
- `get_suppression` — Get one Mailgun suppression or allowlist record.
- `get_template` — Get metadata for one Mailgun template and optionally its active version.
- `get_template_version` — Get content and metadata for one Mailgun template version.
- `list_domains` — List Mailgun domains available to the current API key.
- `list_events` — List delivery, engagement, and failure events for a Mailgun domain.
- `list_suppressions` — List records from a Mailgun suppression or allowlist table.
- `list_template_versions` — List versions for a Mailgun template.
- `list_templates` — List templates stored for a Mailgun domain.
- `send_email` — Send an email through Mailgun using a stored domain. [write]
- `update_domain_tracking_settings` — Update open, click, or unsubscribe tracking settings for a Mailgun domain. [write]
- `verify_domain` — Ask Mailgun to verify DNS records for a sending domain.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Mailgun state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Mailgun is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=mailgun
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Mailgun homepage: https://www.mailgun.com
