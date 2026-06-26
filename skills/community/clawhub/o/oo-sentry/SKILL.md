---
name: oo-sentry
description: "Sentry (sentry.io). Use this skill for ANY Sentry request — reading, creating, and updating data. Whenever a task involves Sentry, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Sentry"
  author: "OOMOL"
  version: "1.0.1"
  services: ["sentry"]
  icon: "https://static.oomol.com/logo/third-party/Sentry.svg"
---

# Sentry

Operate **Sentry** through your OOMOL-connected account. This skill calls the `sentry` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Sentry. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sentry" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sentry" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_alert` — Get one alert workflow in a Sentry organization by workflow id.
- `get_issue` — Get one issue in a Sentry organization by numeric id or short id.
- `get_issue_event` — Get one event for a Sentry issue by event id, or use latest, oldest, or recommended selectors.
- `get_organization_integration` — Get one installed Sentry organization integration by its integration id.
- `get_organization_integration_config` — List available integration provider configs for a Sentry organization, optionally filtered by provider key.
- `get_organization_release` — Get one release in a Sentry organization, with optional health and summary statistics included.
- `get_project` — Get one Sentry project by organization and project slug or id.
- `get_release_health_stats` — Retrieve release health session statistics for one Sentry release by querying the sessions endpoint with that release version.
- `get_replay` — Get one replay instance in a Sentry organization by replay id.
- `get_sentry_app` — Get one Sentry App by id or slug, including integration metadata and OAuth client settings.
- `list_alerts` — List alert workflows for a Sentry organization, with optional id, project, and search filters.
- `list_issue_events` — List events that belong to one Sentry issue, with optional event query filters.
- `list_organization_integrations` — List installed integrations for a Sentry organization, with optional provider and feature filters.
- `list_organization_issues` — List issues for a Sentry organization with optional search, project, and environment filters.
- `list_organization_projects` — List projects that belong to a Sentry organization.
- `list_organization_releases` — List releases that belong to a Sentry organization, optionally filtered by version prefix.
- `list_organization_replays` — List session replays for a Sentry organization, with optional project and environment filters.
- `list_organization_sentry_apps` — List the custom Sentry Apps created by a Sentry organization.
- `update_issue` — Update mutable attributes on one Sentry issue, such as status, assignment, or bookmarks. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Sentry state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Sentry is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=sentry
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Sentry homepage: https://sentry.io
