---
name: oo-folk
description: "folk (folk.app). Use this skill for ANY folk request — reading, creating, updating, and deleting data. Whenever a task involves folk, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "folk"
  author: "OOMOL"
  version: "1.0.1"
  services: ["folk"]
  icon: "https://static.oomol.com/logo/third-party/folk.svg"
---

# folk

Operate **folk** through your OOMOL-connected account. This skill calls the `folk` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected folk. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "folk" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "folk" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_company` — Create one Folk company using the official companies payload fields. [write]
- `create_person` — Create one Folk person using the official people payload fields. [write]
- `delete_company` — Delete one Folk company by company ID. [destructive]
- `delete_person` — Delete one Folk person by person ID. [destructive]
- `get_company` — Get one Folk company by company ID.
- `get_current_user` — Get the current Folk workspace user associated with the API key.
- `get_person` — Get one Folk person by person ID.
- `get_user` — Get one Folk workspace user by user ID.
- `list_companies` — List Folk companies with official cursor pagination and the documented nested filter syntax.
- `list_group_custom_fields` — List Folk custom fields for one group and entity type.
- `list_groups` — List Folk workspace groups with cursor pagination.
- `list_people` — List Folk people with official cursor pagination and the documented nested filter syntax.
- `list_users` — List workspace users from Folk with cursor pagination.
- `update_company` — Update one Folk company by company ID using the official companies payload fields. [write]
- `update_person` — Update one Folk person by person ID using the official people payload fields. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change folk state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — folk is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=folk
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- folk homepage: https://folk.app
