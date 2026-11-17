---
name: oo-securityscorecard
description: "SecurityScorecard (securityscorecard.com). Use this skill for ANY SecurityScorecard request — reading, creating, updating, and deleting data. Whenever a task involves SecurityScorecard, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SecurityScorecard"
  author: "OOMOL"
  version: "1.0.2"
  services: ["securityscorecard"]
  icon: "https://static.oomol.com/logo/third-party/securityscorecard.svg"
---

# SecurityScorecard

Operate **SecurityScorecard** through your OOMOL-connected account. This skill calls the `securityscorecard` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SecurityScorecard. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "securityscorecard" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "securityscorecard" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_portfolio_company` — Add a company to a SecurityScorecard portfolio and request its scorecard if needed. [write]
- `create_portfolio` — Create a SecurityScorecard portfolio for monitoring companies. [write]
- `delete_portfolio` — Delete a SecurityScorecard portfolio. [destructive]
- `get_company` — Get company information and the current SecurityScorecard score summary.
- `get_company_factors` — Get a company security factor scores and issue counts from SecurityScorecard.
- `get_company_score_history` — Get historical SecurityScorecard scores for a company over a date range.
- `list_portfolio_companies` — List companies in a SecurityScorecard portfolio with optional risk filters.
- `list_portfolios` — List all SecurityScorecard portfolios accessible to the connected account.
- `remove_portfolio_company` — Remove a company from a SecurityScorecard portfolio. [write]
- `update_portfolio` — Update a SecurityScorecard portfolio name, description, or visibility. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SecurityScorecard state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SecurityScorecard is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/securityscorecard
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- SecurityScorecard homepage: https://securityscorecard.com/
- API documentation: https://api.securityscorecard.io/api-docs
