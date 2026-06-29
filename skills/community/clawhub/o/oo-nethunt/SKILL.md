---
name: oo-nethunt
description: "NetHunt (nethunt.com). Use this skill for ANY NetHunt request — reading, creating, updating, and deleting data. Whenever a task involves NetHunt, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "NetHunt"
  author: "OOMOL"
  version: "1.0.0"
  services: ["nethunt"]
  icon: "https://static.oomol.com/logo/third-party/nethunt.png"
---

# NetHunt

Operate **NetHunt** through your OOMOL-connected account. This skill calls the `nethunt` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected NetHunt. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "nethunt" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "nethunt" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `auth_test` — Verify the NetHunt credentials and return the connected user.
- `create_call_log` — Create a NetHunt call log on a record. [write]
- `create_comment` — Create a NetHunt comment on a record. [write]
- `create_record` — Create a NetHunt record in a folder with field values. [write]
- `delete_record` — Delete a NetHunt record. [destructive]
- `find_records` — Find NetHunt records by record ID or advanced search query.
- `list_folder_fields` — List fields configured for a NetHunt folder.
- `list_new_call_logs` — List NetHunt call logs created after an optional timestamp.
- `list_new_comments` — List NetHunt record comments created after an optional timestamp.
- `list_new_records` — List NetHunt records created after an optional timestamp.
- `list_readable_folders` — List NetHunt folders that the connected user can read.
- `list_record_changes` — List NetHunt record changes after an optional timestamp.
- `list_updated_records` — List NetHunt records updated after an optional timestamp.
- `list_writable_folders` — List NetHunt folders that the connected user can create records in.
- `update_record` — Update a NetHunt record with field actions. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change NetHunt state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — NetHunt is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=nethunt
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- NetHunt homepage: https://nethunt.com
