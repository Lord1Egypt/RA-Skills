---
name: oo-stannp
description: "Stannp (stannp.com). Use this skill for ANY Stannp request — reading, creating, updating, and deleting data. Whenever a task involves Stannp, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Stannp"
  author: "OOMOL"
  version: "1.0.5"
  services: ["stannp"]
  icon: "https://static.oomol.com/logo/third-party/stannp.svg"
---

# Stannp

Operate **Stannp** through your OOMOL-connected account. This skill calls the `stannp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Stannp. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "stannp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "stannp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_recipients_to_group` — Add one or more existing Stannp recipients to a recipient group. [write]
- `create_group` — Create an empty Stannp recipient group. [write]
- `create_recipient` — Create a Stannp recipient and optionally add it to a group. [write]
- `delete_group` — Delete a Stannp recipient group, optionally deleting its recipients. [destructive]
- `delete_recipient` — Permanently delete a Stannp recipient by ID. [destructive]
- `get_account_balance` — Retrieve the Stannp account balance for the connected regional account.
- `get_recipient` — Retrieve a single Stannp recipient by ID.
- `list_groups` — List Stannp recipient groups with optional offset and limit pagination.
- `list_recipients` — List Stannp recipients, optionally filtered by group and paginated.
- `remove_recipients_from_group` — Remove one or more existing Stannp recipients from a recipient group. [destructive]
- `validate_address` — Validate and normalize a UK, US, or Canadian postal address with Stannp.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Stannp state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Stannp is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/stannp
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Stannp homepage: https://www.stannp.com
- API documentation: https://www.stannp.com/us/direct-mail-api/guide
