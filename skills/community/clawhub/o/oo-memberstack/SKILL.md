---
name: oo-memberstack
description: "Memberstack (memberstack.com). Use this skill for ANY Memberstack request — reading, creating, updating, and deleting data. Whenever a task involves Memberstack, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Memberstack"
  author: "OOMOL"
  version: "1.0.6"
  services: ["memberstack"]
  icon: "https://static.oomol.com/logo/third-party/memberstack.svg"
---

# Memberstack

Operate **Memberstack** through your OOMOL-connected account. This skill calls the `memberstack` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Memberstack. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "memberstack" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "memberstack" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_free_plan` — Add a free Memberstack plan to an existing member. [write]
- `create_member` — Create a Memberstack member with email, optional password, free plans, custom fields, metadata, JSON data, and login redirect. [write]
- `delete_member` — Permanently delete a Memberstack member with optional Stripe customer and subscription cleanup flags. [destructive]
- `get_member` — Retrieve one Memberstack member by member ID or email address, optionally embedding team memberships.
- `list_members` — List Memberstack members with cursor pagination and optional JSON-field inclusion.
- `remove_free_plan` — Remove a free Memberstack plan from an existing member. [destructive]
- `update_member` — Partially update a Memberstack member's email, custom fields, metadata, JSON data, login redirect, verified status, or profile image. [destructive]
- `verify_member_token` — Verify a Memberstack member JWT and return the decoded token payload.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Memberstack state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Memberstack is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/memberstack
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Memberstack homepage: https://www.memberstack.com/
- API documentation: https://developers.memberstack.com/admin-rest-api/quick-start
