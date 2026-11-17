---
name: oo-okta
description: "Okta (okta.com). Use this skill for ANY Okta request — reading, creating, updating, and deleting data. Whenever a task involves Okta, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Okta"
  author: "OOMOL"
  version: "1.0.5"
  services: ["okta"]
  icon: "https://static.oomol.com/logo/third-party/okta.svg"
---

# Okta

Operate **Okta** through your OOMOL-connected account. This skill calls the `okta` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Okta. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "okta" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "okta" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_user_to_group` — Assign an Okta user to an Okta-managed group. [write]
- `create_group` — Create an Okta-managed group. [write]
- `create_user` — Create an Okta user with profile, credentials, group assignments, and activation options. [write]
- `delete_group` — Delete an Okta-managed group by ID. [destructive]
- `delete_user` — Deactivate an active Okta user, or permanently delete a user that is already deactivated. [destructive]
- `get_group` — Get one Okta group by ID.
- `get_user` — Get one Okta user by ID, login, or login shortname.
- `lifecycle_user` — Activate, reactivate, deactivate, suspend, unsuspend, unlock, or expire an Okta user's password.
- `list_group_users` — List the users that are members of an Okta group.
- `list_groups` — List Okta groups with search, filtering, sorting, expansion, and cursor pagination.
- `list_users` — List Okta users with search, filtering, sorting, field projection, and cursor pagination.
- `remove_user_from_group` — Unassign an Okta user from an Okta-managed group. [destructive]
- `update_group` — Replace an Okta-managed group's profile. [destructive]
- `update_user` — Partially update an Okta user's profile or credentials. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Okta state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Okta is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/okta
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Okta homepage: https://www.okta.com/
- API documentation: https://developer.okta.com/docs/api/openapi/okta-management/management/tags/user/
