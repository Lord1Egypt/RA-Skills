---
name: oo-brevo
description: "Brevo (brevo.com). Use this skill for ANY Brevo request — reading, creating, updating, and deleting data. Whenever a task involves Brevo, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Brevo"
  author: "OOMOL"
  version: "1.0.1"
  services: ["brevo"]
  icon: "https://static.oomol.com/logo/third-party/Brevo.svg"
---

# Brevo

Operate **Brevo** through your OOMOL-connected account. This skill calls the `brevo` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Brevo. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "brevo" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "brevo" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_contacts_to_list` — Add contacts to one Brevo contact list using exactly one official selector. [write]
- `create_contact` — Create one Brevo contact with the official contact creation payload. [write]
- `create_contact_list` — Create one Brevo contact list inside the specified Brevo folder. [write]
- `delete_contact` — Delete one Brevo contact by identifier and optional identifier type. [destructive]
- `get_account` — Retrieve the current Brevo account profile and plan information.
- `get_contact` — Retrieve one Brevo contact by identifier and optional identifier type.
- `list_contact_folders` — List Brevo contact folders with the official pagination parameters.
- `list_contact_lists` — List Brevo contact lists with the official pagination parameters.
- `list_contacts` — List Brevo contacts with pagination and timestamp filters.
- `list_contacts_in_list` — List the Brevo contacts currently linked to one Brevo contact list.
- `remove_contacts_from_list` — Remove contacts from one Brevo contact list using exactly one official selector. [destructive]
- `update_contact_list` — Update one Brevo contact list by ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Brevo state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Brevo is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=brevo
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Brevo homepage: https://www.brevo.com
