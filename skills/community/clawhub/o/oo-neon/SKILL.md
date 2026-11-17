---
name: oo-neon
description: "Neon (neon.com). Use this skill for ANY Neon request — reading, creating, updating, and deleting data. Whenever a task involves Neon, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Neon"
  author: "OOMOL"
  version: "1.0.5"
  services: ["neon"]
  icon: "https://static.oomol.com/logo/third-party/Neon.svg"
---

# Neon

Operate **Neon** through your OOMOL-connected account. This skill calls the `neon` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Neon. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "neon" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "neon" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_branch` — Create a branch in a Neon project. [write]
- `create_database` — Create a database in a Neon branch. [write]
- `create_project` — Create a Neon project with an optional default branch configuration. [write]
- `delete_branch` — Delete a branch from a Neon project. [destructive]
- `delete_database` — Delete a database from a Neon branch. [destructive]
- `delete_project` — Delete a Neon project. [destructive]
- `get_branch` — Get detailed metadata for a Neon branch.
- `get_current_user` — Get the currently authenticated Neon user profile.
- `get_database` — Get detailed metadata for a Neon database.
- `get_operation` — Get detailed metadata for a Neon operation.
- `get_project` — Get detailed metadata for a Neon project.
- `list_branches` — List branches for a Neon project.
- `list_databases` — List databases for a Neon branch.
- `list_operations` — List operations for a Neon project.
- `list_projects` — List Neon projects available to the authenticated account.
- `update_branch` — Update a Neon branch name or protection status. [write]
- `update_database` — Update a Neon database name or owner. [write]
- `update_project` — Update a Neon project name or history retention period. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Neon state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Neon is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/neon
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Neon homepage: https://neon.com
- API documentation: https://api-docs.neon.tech/reference/getting-started-with-neon-api
