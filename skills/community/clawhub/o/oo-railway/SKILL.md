---
name: oo-railway
description: "Railway (railway.com). Use this skill for ANY Railway request — reading, creating, updating, and deleting data. Whenever a task involves Railway, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Railway"
  author: "OOMOL"
  version: "1.0.4"
  services: ["railway"]
  icon: "https://static.oomol.com/logo/third-party/railway.png"
---

# Railway

Operate **Railway** through your OOMOL-connected account. This skill calls the `railway` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Railway. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "railway" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "railway" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `deploy_service` — Trigger a Railway deployment for a service, optionally at a specific connected-repository commit. [write]
- `get_deployment` — Get one Railway deployment and its redeploy and rollback capabilities.
- `get_deployment_logs` — Read runtime logs for a Railway deployment with optional text and time filters.
- `get_project` — Get a Railway project together with its services and environments.
- `get_service_instance` — Get Railway service configuration and its latest deployment in one environment.
- `list_deployments` — List recent Railway deployments for a service and environment.
- `list_projects` — List Railway projects available to the configured account or workspace token.
- `rollback_deployment` — Roll a Railway service back to a deployment that Railway marks as rollback-capable. [destructive]
- `upsert_variable` — Create or update one Railway variable for an environment or service. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Railway state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Railway is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/railway
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Railway homepage: https://railway.com
- API documentation: https://docs.railway.com/integrations/api
