---
name: oo-turso
description: "Turso (turso.tech). Use this skill for ANY Turso request — reading, creating, updating, and deleting data. Whenever a task involves Turso, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Turso"
  author: "OOMOL"
  version: "1.0.1"
  services: ["turso"]
  icon: "https://static.oomol.com/logo/third-party/turso.svg"
---

# Turso

Operate **Turso** through your OOMOL-connected account. This skill calls the `turso` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Turso. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "turso" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "turso" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_database` — Create a Turso database in one organization and group. [write]
- `create_group` — Create a Turso group in one organization with a primary location. [write]
- `delete_database` — Delete a Turso database from one organization. [destructive]
- `get_database` — Retrieve one Turso database by name within an organization.
- `get_group` — Retrieve one Turso group by name within an organization.
- `get_organization` — Retrieve one Turso organization by slug.
- `list_databases` — List Turso databases for one organization.
- `list_groups` — List Turso groups for one organization.
- `list_locations` — List available Turso locations that can host groups.
- `list_organizations` — List organizations visible to the current Turso Platform API token.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Turso state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Turso is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=turso
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Turso homepage: https://turso.tech
