---
name: oo-supabase
description: "Supabase (supabase.com). Use this skill for ANY Supabase request — reading, creating, updating, and deleting data. Whenever a task involves Supabase, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Supabase"
  author: "OOMOL"
  version: "1.0.2"
  services: ["supabase"]
  icon: "https://static.oomol.com/logo/third-party/Supabase.svg"
---

# Supabase

Operate **Supabase** through your OOMOL-connected account. This skill calls the `supabase` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Supabase. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "supabase" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "supabase" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_project_api_key` — Create a publishable or secret API key for a Supabase project. [write]
- `delete_project_api_key` — Delete a Supabase project API key. [destructive]
- `delete_project_secrets` — Bulk delete secrets from a Supabase project. [destructive]
- `generate_typescript_types` — Generate TypeScript database types for a Supabase project.
- `get_edge_function` — Get metadata for one Supabase Edge Function by slug.
- `get_organization` — Get details for a Supabase organization by slug.
- `get_project` — Get detailed metadata for a Supabase project by project ref.
- `get_project_api_key` — Get one API key record from a Supabase project.
- `get_project_health` — Check health for selected services in a Supabase project.
- `list_available_regions` — List Supabase regions available for creating projects in an organization.
- `list_edge_functions` — List Edge Functions in a Supabase project.
- `list_organization_members` — List members of a Supabase organization.
- `list_organization_projects` — List projects in a Supabase organization with optional search and pagination.
- `list_organizations` — List the organizations available to the authenticated Supabase account.
- `list_project_api_keys` — List API keys for a Supabase project.
- `list_project_secrets` — List secrets configured for a Supabase project.
- `list_projects` — List Supabase projects visible to the authenticated account.
- `list_storage_buckets` — List Storage buckets for a Supabase project.
- `run_read_only_query` — Run a SQL query through Supabase as the read-only database user.
- `update_project_api_key` — Update the name, description, or JWT template for a Supabase project API key. [write]
- `upsert_project_secrets` — Bulk create or update secrets for a Supabase project. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Supabase state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Supabase is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2, API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=supabase
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Supabase homepage: https://supabase.com
