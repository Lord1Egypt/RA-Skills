---
name: oo-homebox
description: "HomeBox (homebox.software). Use this skill for ANY HomeBox request — reading, creating, updating, and deleting data. Whenever a task involves HomeBox, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "HomeBox"
  author: "OOMOL"
  version: "1.0.2"
  services: ["homebox"]
  icon: "https://static.oomol.com/logo/third-party/homebox.svg"
---

# HomeBox

Operate **HomeBox** through your OOMOL-connected account. This skill calls the `homebox` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected HomeBox. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "homebox" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "homebox" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_entity_attachment` — Download a public file URL and attach the file to one HomeBox entity. [write]
- `add_maintenance_entry` — Add a maintenance entry to one HomeBox entity. [write]
- `create_entity` — Create a new HomeBox entity with a name and optional type, parent, description, quantity, and tags. [write]
- `create_entity_type` — Create a new HomeBox entity type, optionally flagged as a location. [write]
- `create_tag` — Create a new HomeBox tag. [write]
- `delete_entity` — Delete one HomeBox entity. [destructive]
- `delete_entity_type` — Delete one HomeBox entity type. [destructive]
- `delete_tag` — Delete one HomeBox tag. [destructive]
- `get_entity` — Fetch one HomeBox entity with its full details, including attachments and custom fields.
- `get_group_statistics` — Fetch HomeBox group dashboard statistics.
- `get_maintenance_log` — Fetch the maintenance log of one HomeBox entity.
- `get_status` — Fetch the HomeBox instance status: health, version, and whether registration is open.
- `list_custom_field_names` — List custom field names in use across the HomeBox group.
- `list_custom_field_values` — List values in use for one custom field name.
- `list_entities` — Search HomeBox entities with optional text search, pagination, and tag or parent filters.
- `list_entity_types` — List all HomeBox entity types, including location-flagged types.
- `list_tags` — List all HomeBox tags.
- `update_entity` — Update one HomeBox entity while preserving fields that are not provided. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change HomeBox state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — HomeBox is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/homebox
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- HomeBox homepage: https://homebox.software
- API documentation: https://homebox.software/en/api/
