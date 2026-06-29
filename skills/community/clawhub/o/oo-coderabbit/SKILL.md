---
name: oo-coderabbit
description: "CodeRabbit (coderabbit.ai). Use this skill for ANY CodeRabbit request — reading, creating, updating, and deleting data. Whenever a task involves CodeRabbit, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "CodeRabbit"
  author: "OOMOL"
  version: "1.0.0"
  services: ["coderabbit"]
---

# CodeRabbit

Operate **CodeRabbit** through your OOMOL-connected account. This skill calls the `coderabbit` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected CodeRabbit. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "coderabbit" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "coderabbit" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `change_roles` — Bulk change CodeRabbit organization roles for up to 500 users.
- `create_role` — Create a CodeRabbit Enterprise custom role. [write]
- `delete_role` — Delete a CodeRabbit Enterprise custom role when it is not assigned to users. [destructive]
- `get_review_metrics` — Get CodeRabbit merged pull request review metrics for a date range with optional organization, repository, and user filters.
- `get_role` — Get details for one CodeRabbit built-in or Enterprise custom role.
- `get_seat_assignment_mode` — Retrieve the current CodeRabbit seat assignment mode for a self-hosted Enterprise organization.
- `list_audit_logs` — List CodeRabbit organization audit log entries with optional actor, action, resource type, date, and pagination filters.
- `list_role_permissions` — List valid CodeRabbit role permission resource identifiers and access types for custom roles.
- `list_roles` — List CodeRabbit built-in and Enterprise custom roles for the organization.
- `list_users` — List CodeRabbit organization users with optional seat and role filters using cursor-based pagination.
- `manage_seats` — Bulk assign or unassign CodeRabbit seats for up to 500 organization users.
- `update_role` — Update a CodeRabbit Enterprise custom role. [write]
- `update_seat_assignment_mode` — Update the CodeRabbit seat assignment mode for a self-hosted Enterprise organization. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change CodeRabbit state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — CodeRabbit is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=coderabbit
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- CodeRabbit homepage: https://www.coderabbit.ai
