---
name: oo-elasticemail
description: "Elastic Email (elasticemail.com). Use this skill for ANY Elastic Email request — reading, creating, updating, and deleting data. Whenever a task involves Elastic Email, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Elastic Email"
  author: "OOMOL"
  version: "1.0.4"
  services: ["elasticemail"]
  icon: "https://static.oomol.com/logo/third-party/elasticemail.svg"
---

# Elastic Email

Operate **Elastic Email** through your OOMOL-connected account. This skill calls the `elasticemail` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Elastic Email. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "elasticemail" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "elasticemail" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_contacts` — Add up to 1000 contacts to Elastic Email and optionally assign them to lists. [write]
- `add_contacts_to_list` — Add existing Elastic Email contacts to a contact list. [write]
- `create_list` — Create a new Elastic Email contact list. [write]
- `delete_contact` — Delete one Elastic Email contact by email address. [destructive]
- `delete_list` — Delete an Elastic Email list without deleting its contacts. [destructive]
- `get_contact` — Fetch one Elastic Email contact by email address.
- `get_list` — Fetch one Elastic Email contact list by name.
- `list_contacts` — List contacts available to the current Elastic Email API key.
- `list_contacts_in_list` — List contacts that belong to an Elastic Email contact list.
- `list_lists` — List Elastic Email contact lists.
- `remove_contacts_from_list` — Remove Elastic Email contacts from a contact list. [destructive]
- `update_contact` — Update an existing Elastic Email contact by email address. [write]
- `update_list` — Update an existing Elastic Email contact list. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Elastic Email state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Elastic Email is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/elasticemail
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Elastic Email homepage: https://elasticemail.com
- API documentation: https://elasticemail.com/developers/api-documentation/rest-api
