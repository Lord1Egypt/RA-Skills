---
name: oo-kaonavi
description: "Kaonavi (kaonavi.jp). Use this skill for ANY Kaonavi request — reading, creating, updating, and deleting data. Whenever a task involves Kaonavi, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Kaonavi"
  author: "OOMOL"
  version: "1.0.2"
  services: ["kaonavi"]
  icon: "https://static.oomol.com/logo/third-party/kaonavi.svg"
---

# Kaonavi

Operate **Kaonavi** through your OOMOL-connected account. This skill calls the `kaonavi` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Kaonavi. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "kaonavi" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "kaonavi" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `append_sheet_records` — Append records to a multiple-record personnel sheet. Single-record sheets are not supported. [write]
- `create_members` — Create employees with their basic fields and department assignments. Consult get_member_layout for required fields. [write]
- `create_user` — Create a Kaonavi login user linked to an employee. [write]
- `create_users` — Create multiple Kaonavi login users asynchronously. [write]
- `delete_user` — Delete a Kaonavi login user. [destructive]
- `get_enum_options` — Get master options for one custom field.
- `get_member_layout` — Get employee field definitions and required-field settings.
- `get_sheet` — Get personnel sheet records, optionally filtered by member update date.
- `get_sheet_layout` — Get the field layout of a personnel sheet.
- `get_task` — Get the status and messages of an asynchronous Kaonavi task.
- `get_user` — Get a Kaonavi login user by ID.
- `list_departments` — List organizational departments and their parent relationships.
- `list_enum_options` — List master options for custom fields.
- `list_member_photo_urls` — Get employee photo download URLs. Links expire after 15 minutes; request new URLs when needed.
- `list_members` — List employee records, optionally filtered by update date.
- `list_roles` — List available Kaonavi user roles.
- `list_sheet_file_urls` — Get download URLs for files in a sheet attachment field. Only records containing files are returned. Links expire after 15 minutes.
- `list_sheet_layouts` — List accessible personnel sheet layouts and custom field definitions.
- `list_users` — List Kaonavi login users and account settings.
- `update_members` — Update only the supplied employee fields. Omitted fields remain unchanged; use an empty string to clear a value. [write]
- `update_sheet` — Update a personnel sheet. Single-record sheets preserve omitted fields; multiple-record sheets replace the entire record set for each supplied employee. Other employees remain unchanged. [write]
- `update_user` — Update a login user, including role, password, access settings, or disabling the account. Omitted fields remain unchanged. [destructive]
- `update_users` — Update multiple login users asynchronously, including disabling accounts. Omitted fields remain unchanged. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Kaonavi state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Kaonavi is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/kaonavi
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Kaonavi homepage: https://www.kaonavi.jp/
- API documentation: https://developer.kaonavi.jp/api/v2.0/index.html
