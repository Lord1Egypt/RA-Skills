---
name: oo-companycam
description: "CompanyCam (companycam.com). Use this skill for ANY CompanyCam request — reading, creating, updating, and deleting data. Whenever a task involves CompanyCam, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "CompanyCam"
  author: "OOMOL"
  version: "1.0.5"
  services: ["companycam"]
  icon: "https://static.oomol.com/logo/third-party/companycam.png"
---

# CompanyCam

Operate **CompanyCam** through your OOMOL-connected account. This skill calls the `companycam` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected CompanyCam. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "companycam" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "companycam" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `archive_project` — Archive a CompanyCam project by ID. [destructive]
- `create_project` — Create a CompanyCam project with optional address, coordinates, and contact data. [write]
- `create_tag` — Create a CompanyCam tag. [write]
- `delete_tag` — Delete a CompanyCam tag by ID. [destructive]
- `get_company` — Retrieve the CompanyCam company associated with the API token.
- `get_current_user` — Retrieve the current CompanyCam user associated with the API token.
- `get_project` — Retrieve one CompanyCam project by ID.
- `get_tag` — Retrieve one CompanyCam tag by ID.
- `get_user` — Retrieve one CompanyCam user by ID.
- `list_projects` — List CompanyCam projects with optional name, address, and modified-since filters.
- `list_tags` — List CompanyCam tags visible to the API token.
- `list_users` — List CompanyCam users visible to the API token.
- `restore_project` — Restore an archived CompanyCam project by ID. [write]
- `update_project` — Update a CompanyCam project's name, address, coordinates, or geofence. [write]
- `update_tag` — Update a CompanyCam tag label. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change CompanyCam state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — CompanyCam is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/companycam
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- CompanyCam homepage: https://companycam.com
- API documentation: https://companycam.readme.io/docs/getting-started
