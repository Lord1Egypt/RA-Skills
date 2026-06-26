---
name: oo-mailerlite
description: "MailerLite (mailerlite.com). Use this skill for ANY MailerLite request — reading, creating, updating, and deleting data. Whenever a task involves MailerLite, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "MailerLite"
  author: "OOMOL"
  version: "1.0.1"
  services: ["mailerlite"]
  icon: "https://static.oomol.com/logo/third-party/MailerLite.svg"
---

# MailerLite

Operate **MailerLite** through your OOMOL-connected account. This skill calls the `mailerlite` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected MailerLite. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "mailerlite" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "mailerlite" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_subscriber_to_group` — Assign an existing MailerLite subscriber to a MailerLite group. [write]
- `create_group` — Create a new MailerLite group. [write]
- `delete_group` — Delete a MailerLite group by ID. [destructive]
- `delete_subscriber` — Delete a subscriber from the current MailerLite account. [destructive]
- `get_subscriber` — Fetch a single MailerLite subscriber by ID or email.
- `list_fields` — List fields available to the current MailerLite API key.
- `list_group_subscribers` — List subscribers that belong to a MailerLite group.
- `list_groups` — List groups available to the current MailerLite API key.
- `list_subscribers` — List subscribers available to the current MailerLite API key.
- `remove_subscriber_from_group` — Unassign an existing MailerLite subscriber from a MailerLite group. [destructive]
- `update_group` — Update an existing MailerLite group by ID. [write]
- `update_subscriber` — Update an existing MailerLite subscriber by ID. [write]
- `upsert_subscriber` — Create or update a MailerLite subscriber using the official upsert endpoint. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change MailerLite state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — MailerLite is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=mailerlite
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- MailerLite homepage: https://www.mailerlite.com
