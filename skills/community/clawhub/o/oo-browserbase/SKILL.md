---
name: oo-browserbase
description: "Browserbase (browserbase.com). Use this skill for ANY Browserbase request — reading, creating, updating, and deleting data. Whenever a task involves Browserbase, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Browserbase"
  author: "OOMOL"
  version: "1.0.1"
  services: ["browserbase"]
  icon: "https://static.oomol.com/logo/third-party/Browserbase.svg"
---

# Browserbase

Operate **Browserbase** through your OOMOL-connected account. This skill calls the `browserbase` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Browserbase. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "browserbase" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "browserbase" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_context` — Create a Browserbase context and return the upload credentials for an encrypted user-data directory. [write]
- `create_session` — Create a Browserbase session using the connected project by default, with optional context reuse and persistence. [write]
- `delete_context` — Delete one Browserbase context by context identifier. [destructive]
- `get_context` — Get one Browserbase context by context identifier.
- `get_project` — Get one Browserbase project by project identifier.
- `get_project_usage` — Get Browserbase browser minute and proxy byte usage for one project, defaulting to the connected project.
- `get_session` — Get one Browserbase session by session identifier.
- `list_projects` — List the Browserbase projects visible to the current API key.
- `list_sessions` — List Browserbase sessions with optional status or metadata query filters.
- `refresh_context_upload_credentials` — Refresh the Browserbase upload credentials for an existing context so a new encrypted archive can be uploaded. [write]
- `request_session_release` — Request that Browserbase releases a session before timeout by sending status REQUEST_RELEASE.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Browserbase state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Browserbase is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=browserbase
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Browserbase homepage: https://www.browserbase.com
