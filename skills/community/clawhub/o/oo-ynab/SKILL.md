---
name: oo-ynab
description: "YNAB (ynab.com). Use this skill for ANY YNAB request — searching and reading data. Whenever a task involves YNAB, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "YNAB"
  author: "OOMOL"
  version: "1.0.2"
  services: ["ynab"]
  icon: "https://static.oomol.com/logo/third-party/ynab.svg"
---

# YNAB

Operate **YNAB** through your OOMOL-connected account. This skill calls the `ynab` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected YNAB. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "ynab" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "ynab" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_account` — Retrieve a single YNAB account.
- `get_category` — Retrieve a single YNAB category.
- `get_month` — Retrieve a single YNAB plan month.
- `get_month_category` — Retrieve a YNAB category for a specific plan month.
- `get_payee` — Retrieve a single YNAB payee.
- `get_plan` — Retrieve a single YNAB plan with related entities.
- `get_plan_settings` — Retrieve settings for a YNAB plan.
- `get_transaction` — Retrieve a single YNAB transaction.
- `get_user` — Retrieve the authenticated YNAB user.
- `list_accounts` — List accounts for a YNAB plan.
- `list_categories` — List categories grouped by category group for a YNAB plan.
- `list_months` — List months for a YNAB plan.
- `list_payees` — List payees for a YNAB plan.
- `list_plans` — List YNAB plans with summary information.
- `list_transactions` — List YNAB plan transactions.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change YNAB state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — YNAB is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=ynab
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- YNAB homepage: https://www.ynab.com
