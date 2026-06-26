---
name: oo-mailtrap
description: "Mailtrap (mailtrap.io). Use this skill for ANY Mailtrap request — reading, creating, updating, and deleting data. Whenever a task involves Mailtrap, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Mailtrap"
  author: "OOMOL"
  version: "1.0.1"
  services: ["mailtrap"]
  icon: "https://static.oomol.com/logo/third-party/Mailtrap.svg"
---

# Mailtrap

Operate **Mailtrap** through your OOMOL-connected account. This skill calls the `mailtrap` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Mailtrap. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "mailtrap" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "mailtrap" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `clean_inbox` — Delete all messages from one Mailtrap inbox.
- `create_contact` — Create one Mailtrap contact. [write]
- `create_contact_event` — Create one custom Mailtrap contact event. [write]
- `create_contact_export` — Create one Mailtrap contact export job. [write]
- `create_contact_field` — Create one Mailtrap contact field. [write]
- `create_contact_list` — Create one Mailtrap contact list. [write]
- `create_email_template` — Create one Mailtrap email template. [write]
- `create_sending_domain` — Create one Mailtrap sending domain. [write]
- `delete_contact` — Delete one Mailtrap contact by UUID or email. [destructive]
- `delete_contact_field` — Delete one Mailtrap contact field. [destructive]
- `delete_contact_list` — Delete one Mailtrap contact list. [destructive]
- `delete_email_template` — Delete one Mailtrap email template. [destructive]
- `delete_project` — Delete one Mailtrap project. [destructive]
- `delete_sending_domain` — Delete one Mailtrap sending domain. [destructive]
- `get_billing_usage` — Get current Mailtrap billing cycle usage.
- `get_contact` — Get one Mailtrap contact by UUID or email.
- `get_contact_export` — Get one Mailtrap contact export job by ID.
- `get_contact_field` — Get one Mailtrap contact field by ID.
- `get_contact_import` — Get one Mailtrap contact import job by ID. [write]
- `get_contact_list` — Get one Mailtrap contact list by ID.
- `get_email_template` — Get one Mailtrap email template by ID.
- `get_inbox` — Get one Mailtrap inbox by ID.
- `get_message` — Get one Mailtrap inbox message by ID.
- `get_message_html_source` — Get the raw HTML source of one Mailtrap inbox message.
- `get_permission_resources` — Get Mailtrap permission resources accessible to the token.
- `get_project` — Get one Mailtrap project by ID.
- `get_sending_domain` — Get one Mailtrap sending domain by ID.
- `get_sending_stats` — Get Mailtrap sending stats for one account.
- `get_sending_stats_by_categories` — Get Mailtrap sending stats grouped by category.
- `get_sending_stats_by_date` — Get Mailtrap sending stats grouped by date.
- `get_sending_stats_by_domains` — Get Mailtrap sending stats grouped by sending domain.
- `get_sending_stats_by_esp` — Get Mailtrap sending stats grouped by email service provider.
- `import_contacts` — Create one Mailtrap contact import job. [write]
- `list_accounts` — List Mailtrap accounts accessible with the current API token.
- `list_contact_fields` — List Mailtrap contact fields.
- `list_contact_lists` — List Mailtrap contact lists.
- `list_email_templates` — List Mailtrap email templates.
- `list_inboxes` — List Mailtrap inboxes under one account.
- `list_messages` — List messages captured in one Mailtrap inbox.
- `list_projects` — List Mailtrap projects under one account.
- `list_sending_domains` — List Mailtrap sending domains.
- `list_suppressions` — List Mailtrap suppressions.
- `mark_inbox_as_read` — Mark all messages in one Mailtrap inbox as read. [write]
- `reset_inbox_credentials` — Reset SMTP credentials for one Mailtrap inbox. [destructive]
- `update_contact` — Update one Mailtrap contact by UUID or email. [write]
- `update_contact_field` — Update one Mailtrap contact field. [write]
- `update_contact_list` — Update one Mailtrap contact list. [write]
- `update_email_template` — Update one Mailtrap email template. [write]
- `update_inbox` — Update one Mailtrap inbox. [write]
- `update_project` — Update one Mailtrap project. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Mailtrap state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Mailtrap is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=mailtrap
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Mailtrap homepage: https://mailtrap.io/
