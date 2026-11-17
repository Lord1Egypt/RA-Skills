---
name: oo-solarwinds-service-desk
description: "SolarWinds Service Desk (solarwinds.com). Use this skill for ANY SolarWinds Service Desk request — reading, creating, updating, and deleting data. Whenever a task involves SolarWinds Service Desk, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SolarWinds Service Desk"
  author: "OOMOL"
  version: "1.0.2"
  services: ["solarwinds_service_desk"]
  icon: "https://static.oomol.com/logo/third-party/solarwinds_service_desk.svg"
---

# SolarWinds Service Desk

Operate **SolarWinds Service Desk** through your OOMOL-connected account. This skill calls the `solarwinds_service_desk` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SolarWinds Service Desk. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "solarwinds_service_desk" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "solarwinds_service_desk" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_incident` — Create a SolarWinds Service Desk incident with assignment, tags, related resources, and JSON custom fields. [write]
- `create_incident_comment` — Add a public or private comment to a SolarWinds Service Desk incident, optionally triggering notifications. [write]
- `delete_incident` — Delete a SolarWinds Service Desk incident by its resource ID. [destructive]
- `get_incident` — Get a SolarWinds Service Desk incident by ID, optionally including its long-layout details.
- `list_incidents` — List SolarWinds Service Desk incidents with pagination, layout, and creation or update time filters.
- `update_incident` — Update a SolarWinds Service Desk incident, including assignment, custom fields, or a state change that may close it. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SolarWinds Service Desk state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SolarWinds Service Desk is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/solarwinds_service_desk
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- SolarWinds Service Desk homepage: https://www.solarwinds.com/service-desk
- API documentation: https://apidoc.samanage.com/
