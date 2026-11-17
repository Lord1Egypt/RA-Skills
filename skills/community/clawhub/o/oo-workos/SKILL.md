---
name: oo-workos
description: "WorkOS (workos.com). Use this skill for ANY WorkOS request — reading, creating, updating, and deleting data. Whenever a task involves WorkOS, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "WorkOS"
  author: "OOMOL"
  version: "1.0.5"
  services: ["workos"]
  icon: "https://static.oomol.com/logo/third-party/workos.svg"
---

# WorkOS

Operate **WorkOS** through your OOMOL-connected account. This skill calls the `workos` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected WorkOS. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "workos" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "workos" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_organization` — Create a WorkOS organization in the current environment. [write]
- `create_organization_membership` — Create an active WorkOS organization membership for a user and organization. [write]
- `create_user` — Create a WorkOS AuthKit user in the current environment. [write]
- `deactivate_organization_membership` — Deactivate an active WorkOS organization membership. [destructive]
- `get_organization` — Get a WorkOS organization by ID.
- `get_organization_membership` — Get a WorkOS organization membership by ID.
- `get_user` — Get a WorkOS AuthKit user by ID.
- `list_organization_memberships` — List WorkOS organization memberships filtered by user, organization, or membership status.
- `list_organizations` — List WorkOS organizations with optional cursor, domain, and text filters.
- `list_users` — List WorkOS AuthKit users with optional cursor and identity filters.
- `reactivate_organization_membership` — Reactivate an inactive WorkOS organization membership. [write]
- `update_organization` — Update properties of an existing WorkOS organization. [write]
- `update_organization_membership` — Update roles on an existing WorkOS organization membership. [write]
- `update_user` — Update properties of an existing WorkOS AuthKit user. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change WorkOS state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — WorkOS is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/workos
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- WorkOS homepage: https://workos.com
- API documentation: https://workos.com/docs/reference/api-authentication
