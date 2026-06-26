---
name: oo-capsule-crm
description: "Capsule CRM (capsulecrm.com). Use this skill for ANY Capsule CRM request — reading, creating, updating, and deleting data. Whenever a task involves Capsule CRM, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Capsule CRM"
  author: "OOMOL"
  version: "1.0.1"
  services: ["capsule_crm"]
  icon: "https://static.oomol.com/logo/third-party/capsule_crm.svg"
---

# Capsule CRM

Operate **Capsule CRM** through your OOMOL-connected account. This skill calls the `capsule_crm` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Capsule CRM. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "capsule_crm" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "capsule_crm" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_opportunity` — Create a Capsule CRM opportunity. [write]
- `create_party` — Create a Capsule CRM party. [write]
- `create_task` — Create a Capsule CRM task. [write]
- `delete_opportunity` — Delete a Capsule CRM opportunity. [destructive]
- `delete_party` — Delete a Capsule CRM party. [destructive]
- `delete_task` — Delete a Capsule CRM task. [destructive]
- `get_current_user` — Read the Capsule CRM user associated with the access token.
- `get_opportunity` — Read one Capsule CRM opportunity by ID.
- `get_party` — Read one Capsule CRM party by ID.
- `get_task` — Read one Capsule CRM task by ID.
- `list_categories` — List Capsule CRM task categories.
- `list_countries` — List countries supported by Capsule CRM.
- `list_currencies` — List currencies supported by Capsule CRM.
- `list_opportunities` — List Capsule CRM opportunities with pagination, optional change filtering, and embeds.
- `list_parties` — List Capsule CRM parties with pagination, optional change filtering, and embeds.
- `list_pipeline_milestones` — List milestones for a Capsule CRM pipeline.
- `list_pipelines` — List Capsule CRM sales pipelines.
- `list_stages` — List stages for a Capsule CRM board.
- `list_tasks` — List Capsule CRM tasks with pagination, status filtering, and embeds.
- `list_users` — List Capsule CRM users.
- `search_opportunities` — Search Capsule CRM opportunities by query text.
- `search_parties` — Search Capsule CRM parties by query text.
- `update_opportunity` — Update a Capsule CRM opportunity. [write]
- `update_party` — Update a Capsule CRM party. [write]
- `update_task` — Update a Capsule CRM task. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Capsule CRM state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Capsule CRM is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=capsule_crm
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Capsule CRM homepage: https://capsulecrm.com
