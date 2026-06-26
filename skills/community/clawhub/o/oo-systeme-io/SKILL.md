---
name: oo-systeme-io
description: "Systeme.io (systeme.io). Use this skill for ANY Systeme.io request — reading, creating, updating, and deleting data. Whenever a task involves Systeme.io, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Systeme.io"
  author: "OOMOL"
  version: "1.0.1"
  services: ["systeme_io"]
  icon: "https://static.oomol.com/logo/third-party/systeme_io.svg"
---

# Systeme.io

Operate **Systeme.io** through your OOMOL-connected account. This skill calls the `systeme_io` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Systeme.io. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "systeme_io" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "systeme_io" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `attach_contact_tag` — Attach a tag to a contact in Systeme.io.
- `cancel_subscription` — Cancel a subscription in Systeme.io. [write]
- `create_contact` — Create a new contact in Systeme.io. [write]
- `create_enrollment` — Enroll a contact in a course in Systeme.io. [write]
- `create_tag` — Create a new tag in Systeme.io. [write]
- `create_webhook` — Create a new webhook in Systeme.io. [write]
- `delete_contact` — Delete a contact from Systeme.io. [destructive]
- `delete_enrollment` — Remove a contact enrollment from a course in Systeme.io. [destructive]
- `delete_tag` — Delete a tag from Systeme.io. [destructive]
- `delete_webhook` — Delete a webhook from Systeme.io. [destructive]
- `detach_contact_tag` — Detach a tag from a contact in Systeme.io.
- `get_contact` — Get a single contact from Systeme.io by ID.
- `get_tag` — Get a single tag from Systeme.io by ID.
- `get_webhook` — Get a single webhook from Systeme.io by ID.
- `list_contact_fields` — List custom contact fields from Systeme.io.
- `list_contacts` — List contacts from Systeme.io with optional pagination.
- `list_courses` — List courses from Systeme.io with optional pagination.
- `list_enrollments` — List enrollments for a specific course in Systeme.io.
- `list_subscriptions` — List subscriptions from Systeme.io with optional pagination.
- `list_tags` — List tags from Systeme.io with optional pagination.
- `list_webhooks` — List webhooks from Systeme.io with optional pagination.
- `update_contact` — Update an existing contact in Systeme.io. [write]
- `update_tag` — Update an existing tag in Systeme.io. [write]
- `update_webhook` — Update an existing webhook in Systeme.io. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Systeme.io state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Systeme.io is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=systeme_io
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Systeme.io homepage: https://systeme.io
