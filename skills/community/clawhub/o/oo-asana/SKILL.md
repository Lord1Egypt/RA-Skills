---
name: oo-asana
description: "Asana (asana.com). Use this skill for ANY Asana request — reading, creating, and updating data. Whenever a task involves Asana, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Asana"
  author: "OOMOL"
  version: "1.0.1"
  services: ["asana"]
  icon: "https://static.oomol.com/logo/third-party/Asana.svg"
---

# Asana

Operate **Asana** through your OOMOL-connected account. This skill calls the `asana` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Asana. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "asana" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "asana" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_project` — Create an Asana project in a workspace with optional notes, owner, dates, and display settings. [write]
- `create_task` — Create a new Asana task in a project with optional assignee, notes, dates, and custom fields. [write]
- `get_project` — Get a single Asana project by gid.
- `get_task` — Get a single Asana task by gid.
- `get_workspace` — Get a single Asana workspace by gid.
- `list_project_tasks` — List tasks within an Asana project, ordered by project priority, with pagination support.
- `list_projects` — List Asana projects for a workspace, with optional archived filtering and pagination.
- `list_workspaces` — List the Asana workspaces visible to the connected personal access token.
- `update_project` — Update an existing Asana project by gid. [write]
- `update_task` — Update an existing Asana task by gid. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Asana state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Asana is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=asana
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Asana homepage: https://asana.com
