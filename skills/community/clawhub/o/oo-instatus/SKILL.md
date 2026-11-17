---
name: oo-instatus
description: "Instatus (instatus.com). Use this skill for ANY Instatus request — reading, creating, updating, and deleting data. Whenever a task involves Instatus, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Instatus"
  author: "OOMOL"
  version: "1.0.5"
  services: ["instatus"]
  icon: "https://static.oomol.com/logo/third-party/instatus.svg"
---

# Instatus

Operate **Instatus** through your OOMOL-connected account. This skill calls the `instatus` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Instatus. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "instatus" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "instatus" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_component` — Create one component on an Instatus status page. [write]
- `create_incident` — Create one incident on an Instatus status page. [write]
- `create_incident_update` — Create one update on an Instatus incident. [write]
- `delete_component` — Delete one Instatus component by ID. [destructive]
- `delete_incident` — Delete one Instatus incident by ID. [destructive]
- `delete_incident_update` — Delete one Instatus incident update by ID. [destructive]
- `get_component` — Get one Instatus component by ID.
- `get_incident` — Get one Instatus incident by ID.
- `get_incident_update` — Get one Instatus incident update by ID.
- `list_components` — List components on an Instatus status page.
- `list_incidents` — List incidents on an Instatus status page.
- `list_status_pages` — List Instatus status pages in the authenticated account.
- `update_component` — Update one Instatus component by ID. [write]
- `update_incident` — Update one Instatus incident by ID. [write]
- `update_incident_update` — Update one Instatus incident update by ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Instatus state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Instatus is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/instatus
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Instatus homepage: https://instatus.com
- API documentation: https://instatus.com/help/api
