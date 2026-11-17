---
name: oo-auth0-management
description: "Auth0 Management (auth0.com). Use this skill for ANY Auth0 Management request — reading, creating, updating, and deleting data. Whenever a task involves Auth0 Management, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Auth0 Management"
  author: "OOMOL"
  version: "1.0.4"
  services: ["auth0_management"]
  icon: "https://static.oomol.com/logo/third-party/auth0_management.svg"
---

# Auth0 Management

Operate **Auth0 Management** through your OOMOL-connected account. This skill calls the `auth0_management` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Auth0 Management. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "auth0_management" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "auth0_management" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_permissions_to_role` — Associate one or more Auth0 permissions with a role. [write]
- `assign_roles_to_user` — Assign one or more Auth0 roles to a user. [write]
- `get_role` — Retrieve one Auth0 role by role ID.
- `get_user` — Retrieve one Auth0 user by user ID.
- `list_role_permissions` — List permissions granted by an Auth0 role.
- `list_role_users` — List users assigned to an Auth0 role with offset or checkpoint pagination.
- `list_roles` — List Auth0 roles with pagination and optional name filter.
- `list_user_effective_permissions` — List Auth0 permissions granted to a user directly or through roles or groups.
- `list_user_effective_roles` — List Auth0 roles granted to a user directly or through group membership.
- `list_user_permissions` — List permissions directly assigned to an Auth0 user.
- `list_user_roles` — List Auth0 roles assigned to a user.
- `list_users` — List Auth0 users with pagination and optional Lucene search query.
- `remove_permissions_from_role` — Remove one or more Auth0 permissions from a role. [destructive]
- `remove_roles_from_user` — Remove one or more Auth0 roles from a user. [destructive]
- `search_users_by_email` — Search Auth0 users by email with the official users-by-email endpoint.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Auth0 Management state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Auth0 Management is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/auth0_management
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Auth0 Management homepage: https://auth0.com
- API documentation: https://auth0.com/docs/api/management/v2
