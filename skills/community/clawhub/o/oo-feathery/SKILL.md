---
name: oo-feathery
description: "Feathery (feathery.io). Use this skill for ANY Feathery request — reading, creating, updating, and deleting data. Whenever a task involves Feathery, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Feathery"
  author: "OOMOL"
  version: "1.0.1"
  services: ["feathery"]
  icon: "https://static.oomol.com/logo/third-party/feathery.png"
---

# Feathery

Operate **Feathery** through your OOMOL-connected account. This skill calls the `feathery` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Feathery. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "feathery" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "feathery" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_hidden_field` — Create a Feathery hidden field by field ID. [write]
- `create_or_fetch_user` — Create a Feathery user or fetch the existing user by ID. [write]
- `create_or_update_form_submissions` — Create or update Feathery form submissions for one form. [write]
- `delete_hidden_field` — Delete one Feathery hidden field by field ID. [destructive]
- `delete_user` — Delete one Feathery user by ID. [destructive]
- `edit_hidden_field` — Rename or edit a Feathery hidden field by field ID. [write]
- `get_account_info` — Retrieve Feathery team and account information for the authenticated API key.
- `get_form_schema` — Retrieve the complete schema for one Feathery form.
- `get_user_data` — Retrieve all Feathery field data, optionally scoped to one user.
- `get_user_session` — Retrieve Feathery form session and progress data for one user.
- `list_forms` — List Feathery forms, optionally filtered by tags.
- `list_hidden_fields` — List hidden fields configured in the Feathery account.
- `list_users` — List Feathery users with optional creation-time and field-value filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Feathery state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Feathery is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=feathery
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Feathery homepage: https://www.feathery.io/
