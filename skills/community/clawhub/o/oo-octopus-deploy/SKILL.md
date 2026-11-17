---
name: oo-octopus-deploy
description: "Octopus Deploy (octopus.com). Use this skill for ANY Octopus Deploy request — searching and reading data. Whenever a task involves Octopus Deploy, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Octopus Deploy"
  author: "OOMOL"
  version: "1.0.5"
  services: ["octopus_deploy"]
  icon: "https://static.oomol.com/logo/third-party/octopus_deploy.svg"
---

# Octopus Deploy

Operate **Octopus Deploy** through your OOMOL-connected account. This skill calls the `octopus_deploy` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Octopus Deploy. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "octopus_deploy" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "octopus_deploy" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_current_user` — Fetch the current Octopus Deploy user for the connected API key.
- `get_deployment` — Fetch one deployment inside an Octopus Deploy space by ID.
- `get_environment` — Fetch one environment inside an Octopus Deploy space by ID.
- `get_project` — Fetch one project inside an Octopus Deploy space by ID.
- `get_release` — Fetch one release inside an Octopus Deploy space by ID.
- `get_task` — Fetch one Octopus Deploy server task inside a space by ID.
- `list_deployments` — List deployments inside an Octopus Deploy space with optional filters.
- `list_environments` — List environments inside an Octopus Deploy space.
- `list_projects` — List projects inside an Octopus Deploy space.
- `list_releases` — List releases inside an Octopus Deploy space.
- `list_spaces` — List Octopus Deploy spaces visible to the connected API key.
- `list_tasks` — List Octopus Deploy server tasks inside a space with optional filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Octopus Deploy state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Octopus Deploy is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/octopus_deploy
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Octopus Deploy homepage: https://octopus.com
- API documentation: https://octopus.com/docs/octopus-rest-api/getting-started
