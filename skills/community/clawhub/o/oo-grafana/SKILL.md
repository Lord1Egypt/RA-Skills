---
name: oo-grafana
description: "Grafana (grafana.com). Use this skill for ANY Grafana request — reading, creating, updating, and deleting data. Whenever a task involves Grafana, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Grafana"
  author: "OOMOL"
  version: "1.0.1"
  services: ["grafana"]
  icon: "https://static.oomol.com/logo/third-party/grafana.svg"
---

# Grafana

Operate **Grafana** through your OOMOL-connected account. This skill calls the `grafana` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Grafana. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "grafana" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "grafana" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_dashboard` — Create a Grafana dashboard resource in a namespace. [write]
- `create_data_source` — Create a Grafana data source using a JSON payload accepted by Grafana. [write]
- `create_folder` — Create a Grafana folder in a namespace. [write]
- `delete_dashboard` — Delete a Grafana dashboard resource by UID. [destructive]
- `delete_data_source` — Delete a Grafana data source by UID. [destructive]
- `delete_folder` — Delete a Grafana folder by UID. [destructive]
- `get_dashboard` — Retrieve one Grafana dashboard resource by UID.
- `get_data_source` — Retrieve one Grafana data source by UID.
- `get_folder` — Retrieve one Grafana folder by UID.
- `list_data_sources` — List Grafana data sources available to the service account token.
- `list_folders` — List Grafana folders in a namespace with optional pagination.
- `search_dashboards` — Search Grafana folders and dashboards by query, tags, type, folder, and pagination.
- `update_dashboard` — Replace a Grafana dashboard resource by UID. [write]
- `update_data_source` — Update a Grafana data source by UID using fields accepted by Grafana. [write]
- `update_folder` — Update the title or parent folder for a Grafana folder. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Grafana state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Grafana is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=grafana
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Grafana homepage: https://grafana.com
