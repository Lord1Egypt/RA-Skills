---
name: oo-postmark
description: "Postmark (postmarkapp.com). Use this skill for ANY Postmark request — reading, creating, and updating data. Whenever a task involves Postmark, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Postmark"
  author: "OOMOL"
  version: "1.0.1"
  services: ["postmark"]
  icon: "https://static.oomol.com/logo/third-party/Postmark.svg"
---

# Postmark

Operate **Postmark** through your OOMOL-connected account. This skill calls the `postmark` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Postmark. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "postmark" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "postmark" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_template` — Create a new template in the current Postmark server. [write]
- `edit_template` — Edit an existing Postmark template by template ID or alias. [write]
- `get_bounces` — Get Postmark bounces for the current server with optional filters.
- `get_outbound_message_details` — Get detailed content and events for one outbound Postmark message.
- `get_server` — Get the current Postmark server configuration for the connected server token.
- `get_template` — Get one Postmark template by template ID or alias.
- `list_templates` — List templates available in the current Postmark server.
- `search_outbound_messages` — Search outbound Postmark messages with filters and pagination.
- `send_batch_with_templates` — Send up to 500 templated emails in a single Postmark batch request. [write]
- `send_email` — Send a transactional email through the current Postmark server. [write]
- `send_email_with_template` — Send a single templated email through the current Postmark server. [write]
- `validate_template` — Validate Postmark template content against the official template renderer.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Postmark state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Postmark is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=postmark
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Postmark homepage: https://postmarkapp.com
