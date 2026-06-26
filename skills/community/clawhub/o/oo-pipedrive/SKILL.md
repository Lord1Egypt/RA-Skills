---
name: oo-pipedrive
description: "Pipedrive (pipedrive.com). Use this skill for ANY Pipedrive request — reading, creating, updating, and deleting data. Whenever a task involves Pipedrive, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Pipedrive"
  author: "OOMOL"
  version: "1.0.1"
  services: ["pipedrive"]
  icon: "https://static.oomol.com/logo/third-party/Pipedrive.svg"
---

# Pipedrive

Operate **Pipedrive** through your OOMOL-connected account. This skill calls the `pipedrive` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Pipedrive. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "pipedrive" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "pipedrive" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_activity` — Create a Pipedrive activity with subject, due date, linked records, participants, attendees, and notes. [write]
- `create_deal` — Create a Pipedrive deal with title, contact links, pipeline placement, labels, and optional custom fields. [write]
- `create_organization` — Create a Pipedrive organization with optional labels, address, and custom fields. [write]
- `create_person` — Create a Pipedrive person with emails, phones, labels, and optional custom fields. [write]
- `delete_activity` — Delete one Pipedrive activity by activity ID. [destructive]
- `delete_deal` — Delete one Pipedrive deal by deal ID. [destructive]
- `delete_organization` — Delete one Pipedrive organization by organization ID. [destructive]
- `delete_person` — Delete one Pipedrive person by person ID. [destructive]
- `get_activity` — Get one Pipedrive activity by activity ID.
- `get_deal` — Get one Pipedrive deal by deal ID.
- `get_organization` — Get one Pipedrive organization by organization ID.
- `get_person` — Get one Pipedrive person by person ID.
- `get_pipeline` — Get one Pipedrive pipeline by pipeline ID.
- `get_stage` — Get one Pipedrive stage by stage ID.
- `list_activities` — List Pipedrive activities with optional owner, contact, deal, completion, and pagination filters.
- `list_deals` — List Pipedrive deals with optional owner, contact, pipeline, stage, status, and pagination filters.
- `list_organizations` — List Pipedrive organizations with optional owner, custom field, and pagination filters.
- `list_persons` — List Pipedrive persons with optional owner, organization, deal, custom field, and pagination filters.
- `list_pipelines` — List Pipedrive pipelines with optional sorting and pagination.
- `list_stages` — List Pipedrive stages with optional pipeline, sorting, and pagination filters.
- `search_deals` — Search Pipedrive deals by title, notes, or custom fields.
- `search_organizations` — Search Pipedrive organizations by name, address, notes, or custom fields.
- `search_persons` — Search Pipedrive persons by name, email, phone, notes, or custom fields.
- `update_activity` — Update one Pipedrive activity by activity ID. [write]
- `update_deal` — Update one Pipedrive deal by deal ID. [write]
- `update_organization` — Update one Pipedrive organization by organization ID. [write]
- `update_person` — Update one Pipedrive person by person ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Pipedrive state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Pipedrive is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=pipedrive
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Pipedrive homepage: https://www.pipedrive.com
