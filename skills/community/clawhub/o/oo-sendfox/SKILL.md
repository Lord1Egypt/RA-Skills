---
name: oo-sendfox
description: "SendFox (sendfox.com). Use this skill for ANY SendFox request — reading, creating, updating, and deleting data. Whenever a task involves SendFox, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SendFox"
  author: "OOMOL"
  version: "1.0.1"
  services: ["sendfox"]
  icon: "https://static.oomol.com/logo/third-party/sendfox.svg"
---

# SendFox

Operate **SendFox** through your OOMOL-connected account. This skill calls the `sendfox` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SendFox. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sendfox" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sendfox" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_contact_to_list` — Add an existing SendFox contact to a contact list. [write]
- `create_contact` — Create a SendFox contact and optionally attach it to lists with custom contact fields. [write]
- `create_contact_list` — Create a SendFox contact list. [write]
- `delete_contact` — Soft-delete a SendFox contact and cancel any scheduled deliverables. [destructive]
- `delete_contact_list` — Soft-delete a SendFox contact list when it is not used by dependent resources. [destructive]
- `get_contact` — Get a SendFox contact by ID.
- `get_contact_list` — Get a SendFox contact list by ID.
- `list_contact_lists` — List SendFox contact lists with optional search filtering.
- `list_contacts` — List SendFox contacts with optional search, email, and unsubscribe filters.
- `list_contacts_in_list` — List contacts in a SendFox contact list with optional search filtering.
- `remove_contact_from_list` — Remove a SendFox contact from a contact list. [destructive]
- `unsubscribe_contact` — Unsubscribe a SendFox contact by email address. [destructive]
- `update_contact` — Update a SendFox contact's name, list memberships, or custom field values. [write]
- `update_contact_list` — Update a SendFox contact list name. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SendFox state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SendFox is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=sendfox
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- SendFox homepage: https://sendfox.com
