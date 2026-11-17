---
name: oo-ninjapear
description: "NinjaPear (nubela.co). Use this skill for ANY NinjaPear request — searching and reading data. Whenever a task involves NinjaPear, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "NinjaPear"
  author: "OOMOL"
  version: "1.0.4"
  services: ["ninjapear"]
  icon: "https://static.oomol.com/logo/third-party/ninjapear.svg"
---

# NinjaPear

Operate **NinjaPear** through your OOMOL-connected account. This skill calls the `ninjapear` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected NinjaPear. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "ninjapear" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "ninjapear" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `check_disposable_email` — Check whether an email address is disposable or from a free email provider.
- `get_company_details` — Retrieve detailed company information such as description, industry, leadership, and addresses.
- `get_credit_balance` — Get the current NinjaPear credit balance for the authenticated account.
- `get_employee_count` — Get the estimated employee count for a company.
- `list_competitors` — Discover direct business competitors of a target company.
- `list_customers` — List likely customers, investors, and partner platforms for a target company.
- `list_products` — List products and services offered by a target company.
- `lookup_company_website` — Resolve a company name to its canonical website URL.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change NinjaPear state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — NinjaPear is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/ninjapear
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- NinjaPear homepage: https://nubela.co/
- API documentation: https://nubela.co/docs
