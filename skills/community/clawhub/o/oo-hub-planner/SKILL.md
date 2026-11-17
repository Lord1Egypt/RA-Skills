---
name: oo-hub-planner
description: "Resource Flow (Hub Planner) (milientsoftware.com). Use this skill for ANY Resource Flow (Hub Planner) request — reading, creating, and updating data. Whenever a task involves Resource Flow (Hub Planner), use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Resource Flow (Hub Planner)"
  author: "OOMOL"
  version: "1.0.4"
  services: ["hub_planner"]
  icon: "https://static.oomol.com/logo/third-party/hub_planner.svg"
---

# Resource Flow (Hub Planner)

Operate **Resource Flow (Hub Planner)** through your OOMOL-connected account. This skill calls the `hub_planner` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Resource Flow (Hub Planner). **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "hub_planner" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "hub_planner" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_project` — Create a Hub Planner project with core scheduling and budget fields. [write]
- `create_resource` — Create a Hub Planner resource and optionally send an invitation email. [write]
- `get_project` — Get one Hub Planner project by its unique ID.
- `get_resource` — Get one Hub Planner resource by its unique ID.
- `list_projects` — List Hub Planner projects with optional zero-based pagination and sorting.
- `list_resources` — List Hub Planner resources with optional zero-based pagination and sorting.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Resource Flow (Hub Planner) state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Resource Flow (Hub Planner) is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/hub_planner
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Resource Flow (Hub Planner) homepage: https://www.milientsoftware.com/hub-planner
- API documentation: https://api-docs.hubplanner.com/
