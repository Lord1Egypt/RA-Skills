---
name: oo-surecontact
description: "SureContact (surecontact.com). Use this skill for ANY SureContact request — reading, creating, updating, and deleting data. Whenever a task involves SureContact, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SureContact"
  author: "OOMOL"
  version: "1.0.5"
  services: ["surecontact"]
  icon: "https://static.oomol.com/logo/third-party/surecontact.svg"
---

# SureContact

Operate **SureContact** through your OOMOL-connected account. This skill calls the `surecontact` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SureContact. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "surecontact" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "surecontact" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_contacts_to_list` — Add one or more SureContact contacts to a list. [write]
- `attach_contact_lists` — Attach one or more SureContact lists to a contact. [write]
- `attach_contact_tags` — Attach one or more SureContact tags to a contact. [write]
- `create_contact` — Create a SureContact contact and optionally attach lists or tags. [write]
- `create_list` — Create a SureContact list. [write]
- `create_tag` — Create a SureContact tag. [write]
- `delete_contact` — Delete a SureContact contact by UUID. [destructive]
- `delete_list` — Delete a SureContact list by UUID. [destructive]
- `delete_tag` — Delete a SureContact tag by UUID. [destructive]
- `detach_contact_lists` — Detach one or more SureContact lists from a contact. [destructive]
- `detach_contact_tags` — Detach one or more SureContact tags from a contact. [destructive]
- `get_contact` — Retrieve one SureContact contact by UUID.
- `get_contact_by_email` — Retrieve one SureContact contact by email address.
- `get_list` — Retrieve one SureContact list by UUID.
- `get_tag` — Retrieve one SureContact tag by UUID.
- `list_contacts` — List SureContact contacts with optional search, status, list, tag, and pagination filters.
- `list_lists` — List SureContact lists with optional search and pagination filters.
- `list_tags` — List SureContact tags with optional search and pagination filters.
- `remove_contacts_from_list` — Remove one or more SureContact contacts from a list. [destructive]
- `update_contact` — Update a SureContact contact by UUID. [write]
- `update_list` — Update a SureContact list by UUID. [write]
- `update_tag` — Update a SureContact tag by UUID. [write]
- `upsert_contact` — Create or update a SureContact contact by email address. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SureContact state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SureContact is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/surecontact
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- SureContact homepage: https://surecontact.com/
- API documentation: https://api.surecontact.com/docs
