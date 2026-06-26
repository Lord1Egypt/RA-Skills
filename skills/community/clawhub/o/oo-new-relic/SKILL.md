---
name: oo-new-relic
description: "New Relic (newrelic.com). Use this skill for ANY New Relic request — reading, creating, updating, and deleting data. Whenever a task involves New Relic, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "New Relic"
  author: "OOMOL"
  version: "1.0.1"
  services: ["new_relic"]
  icon: "https://static.oomol.com/logo/third-party/New%20Relic.svg"
---

# New Relic

Operate **New Relic** through your OOMOL-connected account. This skill calls the `new_relic` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected New Relic. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "new_relic" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "new_relic" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_alert_policy` — Create a New Relic alert policy using the REST alerts API. [write]
- `create_dashboard` — Create a New Relic dashboard with pages and widgets using NerdGraph. [write]
- `create_dashboard_snapshot_url` — Generate a snapshot URL for a New Relic dashboard page GUID. [write]
- `create_deployment_marker` — Create a New Relic change-tracking deployment marker for an entity GUID using NerdGraph. [write]
- `create_nrql_condition` — Create a static or baseline NRQL alert condition for a policy using the REST alerts API. [write]
- `create_secure_credential` — Create a New Relic synthetic secure credential using NerdGraph. [write]
- `create_synthetics_simple_monitor` — Create a New Relic ping monitor by using the syntheticsCreateSimpleMonitor mutation. [write]
- `delete_alert_policy` — Delete a New Relic alert policy using the REST alerts API. [destructive]
- `delete_dashboard` — Delete a New Relic dashboard by its entity GUID. [destructive]
- `delete_nrql_condition` — Delete a New Relic NRQL alert condition using the REST alerts API. [destructive]
- `delete_secure_credential` — Delete a New Relic synthetic secure credential using NerdGraph. [destructive]
- `delete_synthetics_monitor` — Delete a synthetic monitor by GUID using the syntheticsDeleteMonitor mutation. [destructive]
- `execute_nrql_query` — Execute an NRQL query against a specific New Relic account and return the query results and metadata.
- `get_alert_policies` — List New Relic alert policies with optional name, incident preference, and pagination filters using the REST alerts API.
- `get_current_user` — Validate the connected New Relic user key and return the current user profile from NerdGraph.
- `get_dashboard_entity` — Read a New Relic dashboard entity, including its pages and widgets, by GUID.
- `get_secure_credential` — Get a synthetic secure credential by key using NerdGraph entity search metadata only.
- `get_synth_monitor` — Get a synthetic monitor by its legacy monitor ID or entity GUID using NerdGraph entity search.
- `list_deployments` — List deployment markers for a legacy APM application by using the REST v2 deployments API.
- `list_monitors` — List synthetic monitors by using NerdGraph entity search over the SYNTH MONITOR entity type.
- `list_nrql_conditions` — List NRQL alert conditions for a specific alert policy using the REST alerts API.
- `list_secure_credentials` — List synthetic secure credentials by using NerdGraph entity search over the SYNTH SECURE_CRED entity type.
- `search_entities` — Search New Relic entities with either the raw entity search language or a structured query builder.
- `update_alert_policy` — Update a New Relic alert policy name or incident preference using the REST alerts API. [write]
- `update_dashboard` — Update a New Relic dashboard by GUID, replacing the dashboard configuration with the supplied pages and widgets. [write]
- `update_nrql_condition` — Update a static or baseline NRQL alert condition using the REST alerts API. [write]
- `update_secure_credential` — Update a New Relic synthetic secure credential value or description using NerdGraph. [write]
- `update_synthetics_simple_monitor` — Update a New Relic ping monitor by GUID using the syntheticsUpdateSimpleMonitor mutation. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change New Relic state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — New Relic is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=new_relic
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- New Relic homepage: https://newrelic.com
