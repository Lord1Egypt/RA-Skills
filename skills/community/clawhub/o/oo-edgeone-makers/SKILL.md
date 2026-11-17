---
name: oo-edgeone-makers
description: "EdgeOne Makers (edgeone.ai). Use this skill for ANY EdgeOne Makers request — reading, creating, updating, and deleting data. Whenever a task involves EdgeOne Makers, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "EdgeOne Makers"
  author: "OOMOL"
  version: "1.0.2"
  services: ["edgeone_makers"]
  icon: "https://static.oomol.com/logo/third-party/edgeone_makers.png"
---

# EdgeOne Makers

Operate **EdgeOne Makers** through your OOMOL-connected account. This skill calls the `edgeone_makers` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected EdgeOne Makers. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "edgeone_makers" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "edgeone_makers" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `delete_environment_variables` — Delete environment variables from an EdgeOne Makers project. [destructive]
- `delete_project` — Delete an EdgeOne Makers project and its deployment history. [destructive]
- `get_deployment` — Get an EdgeOne Makers deployment and its current status.
- `get_deployment_log` — Get the build log URL for an EdgeOne Makers deployment.
- `get_project` — Get an EdgeOne Makers project by ID.
- `list_deployments` — List deployments for an EdgeOne Makers project.
- `list_environment_variables` — List environment variables configured for an EdgeOne Makers project.
- `list_projects` — List EdgeOne Makers projects available to the connected account.
- `set_environment_variables` — Add or overwrite environment variables for an EdgeOne Makers project while preserving unmentioned variables. [destructive]
- `trigger_deployment_webhook` — Trigger a deployment through an EdgeOne Makers project deployment webhook. [write]
- `update_project` — Update an EdgeOne Makers project's name or build configuration. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change EdgeOne Makers state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — EdgeOne Makers is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/edgeone_makers
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- EdgeOne Makers homepage: https://edgeone.ai/zh/products/pages
- API documentation: https://pages.edgeone.ai/document/overview
