---
name: oo-simpletexting
description: "SimpleTexting (simpletexting.com). Use this skill for ANY SimpleTexting request — reading, creating, updating, and deleting data. Whenever a task involves SimpleTexting, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SimpleTexting"
  author: "OOMOL"
  version: "1.0.2"
  services: ["simpletexting"]
  icon: "https://static.oomol.com/logo/third-party/simpletexting.svg"
---

# SimpleTexting

Operate **SimpleTexting** through your OOMOL-connected account. This skill calls the `simpletexting` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SimpleTexting. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "simpletexting" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "simpletexting" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_contact_to_list` — Add an existing SimpleTexting contact to a contact list. [write]
- `create_contact` — Create a SimpleTexting contact, or update an existing contact when upsert is enabled. [write]
- `create_contact_list` — Create a SimpleTexting contact list. [write]
- `delete_contact` — Delete a SimpleTexting contact by phone number or ID. [destructive]
- `delete_contact_list` — Delete a SimpleTexting contact list by ID or name. [destructive]
- `get_account` — Get the SimpleTexting account email associated with the connected API token.
- `get_contact` — Get a SimpleTexting contact by phone number or ID.
- `get_contact_list` — Get a SimpleTexting contact list by ID or name.
- `list_contact_lists` — List one page of SimpleTexting contact lists.
- `list_contacts` — List one page of SimpleTexting contacts, optionally updated since a timestamp.
- `list_custom_fields` — List one page of SimpleTexting custom fields and their merge tags.
- `list_segments` — List one page of SimpleTexting contact segments.
- `remove_contact_from_list` — Remove a contact from a SimpleTexting list without deleting the contact. [write]
- `update_contact` — Update a SimpleTexting contact and optionally replace or add list memberships. [write]
- `update_contact_list` — Rename a SimpleTexting contact list by ID or existing name. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SimpleTexting state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SimpleTexting is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/simpletexting
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- SimpleTexting homepage: https://simpletexting.com/
- API documentation: https://simpletexting.com/api/docs/v2/
