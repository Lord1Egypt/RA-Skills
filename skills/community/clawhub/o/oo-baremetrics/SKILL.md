---
name: oo-baremetrics
description: "Baremetrics (baremetrics.com). Use this skill for ANY Baremetrics request — reading, creating, updating, and deleting data. Whenever a task involves Baremetrics, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Baremetrics"
  author: "OOMOL"
  version: "1.0.5"
  services: ["baremetrics"]
  icon: "https://static.oomol.com/logo/third-party/baremetrics.png"
---

# Baremetrics

Operate **Baremetrics** through your OOMOL-connected account. This skill calls the `baremetrics` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Baremetrics. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "baremetrics" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "baremetrics" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_subscription` — Cancel a Baremetrics subscription at a documented cancellation timestamp. [destructive]
- `create_customer` — Create a customer record in a Baremetrics API source. [write]
- `create_plan` — Create a plan for use in Baremetrics subscription records. [write]
- `create_subscription` — Create a subscription in a Baremetrics API source. [write]
- `list_charges` — List charges for a Baremetrics source with optional time and entity filters.
- `list_customers` — List customers for a Baremetrics source with optional search and ordering.
- `list_plans` — List plans for a Baremetrics source with optional search.
- `list_sources` — List Baremetrics sources available to the current API key.
- `list_subscriptions` — List subscriptions for a Baremetrics source with optional customer and ordering filters.
- `update_customer` — Update basic information for a Baremetrics customer. [write]
- `update_plan` — Update the name of a Baremetrics plan. [write]
- `update_subscription` — Update plan, addon, quantity, or discount data for a Baremetrics subscription. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Baremetrics state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Baremetrics is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/baremetrics
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Baremetrics homepage: https://baremetrics.com
- API documentation: https://developers.baremetrics.com/reference
