---
name: oo-central-station-crm
description: "CentralStationCRM (centralstationcrm.de). Use this skill for ANY CentralStationCRM request — reading, creating, updating, and deleting data. Whenever a task involves CentralStationCRM, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "CentralStationCRM"
  author: "OOMOL"
  version: "1.0.4"
  services: ["central_station_crm"]
  icon: "https://static.oomol.com/logo/third-party/central_station_crm.svg"
---

# CentralStationCRM

Operate **CentralStationCRM** through your OOMOL-connected account. This skill calls the `central_station_crm` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected CentralStationCRM. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "central_station_crm" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "central_station_crm" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_company` — Create a company in CentralStationCRM. [write]
- `create_deal` — Create a deal in CentralStationCRM. [write]
- `create_person` — Create a person in CentralStationCRM. [write]
- `delete_company` — Delete a company from CentralStationCRM. [destructive]
- `delete_deal` — Delete a deal from CentralStationCRM. [destructive]
- `delete_person` — Delete a person from CentralStationCRM. [destructive]
- `get_company` — Get one CentralStationCRM company by identifier.
- `get_deal` — Get one CentralStationCRM deal by identifier.
- `get_person` — Get one CentralStationCRM person by identifier.
- `get_user` — Get the current CentralStationCRM API user.
- `list_companies` — List companies in CentralStationCRM with optional paging and tag filters.
- `list_deals` — List deals in CentralStationCRM with optional paging and tag filters.
- `list_people` — List people in CentralStationCRM with optional paging and tag filters.
- `search_companies` — Search CentralStationCRM companies by documented search fields.
- `search_deals` — Search CentralStationCRM deals by documented search fields.
- `search_people` — Search CentralStationCRM people by documented search fields.
- `update_company` — Update a company in CentralStationCRM. [write]
- `update_deal` — Update a deal in CentralStationCRM. [write]
- `update_person` — Update a person in CentralStationCRM. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change CentralStationCRM state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — CentralStationCRM is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/central_station_crm
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- CentralStationCRM homepage: https://centralstationcrm.de
- API documentation: https://api.centralstationcrm.net/api-docs/index.html
