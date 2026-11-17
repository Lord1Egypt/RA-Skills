---
name: oo-active-trail
description: "ActiveTrail (activetrail.com). Use this skill for ANY ActiveTrail request — reading, creating, updating, and deleting data. Whenever a task involves ActiveTrail, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "ActiveTrail"
  author: "OOMOL"
  version: "1.0.5"
  services: ["active_trail"]
  icon: "https://static.oomol.com/logo/third-party/active_trail.svg"
---

# ActiveTrail

Operate **ActiveTrail** through your OOMOL-connected account. This skill calls the `active_trail` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected ActiveTrail. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "active_trail" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "active_trail" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_group_member` — Add or update a contact inside an ActiveTrail group. [write]
- `create_contact` — Create an ActiveTrail contact. [write]
- `create_group` — Create an ActiveTrail group. [write]
- `delete_contact` — Delete one ActiveTrail contact by ID. [destructive]
- `delete_group` — Delete one ActiveTrail group by ID. [destructive]
- `get_account_balance` — Fetch the current ActiveTrail email, SMS, and coupon account balances.
- `get_contact` — Fetch one ActiveTrail contact by ID.
- `get_group` — Fetch one ActiveTrail group by ID.
- `list_contacts` — List ActiveTrail contacts with optional state, search, date, and pagination filters.
- `list_group_members` — List members in an ActiveTrail group with optional filters.
- `list_groups` — List ActiveTrail groups with optional search and pagination filters.
- `remove_group_member` — Remove one contact from an ActiveTrail group. [destructive]
- `update_contact` — Update an ActiveTrail contact. [write]
- `update_group` — Update an ActiveTrail group name. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change ActiveTrail state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — ActiveTrail is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/active_trail
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- ActiveTrail homepage: https://www.activetrail.com/
- API documentation: https://webapi.mymarketing.co.il/api/docs/Guides
