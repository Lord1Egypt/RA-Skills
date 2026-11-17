---
name: oo-moneyforward-mcp
description: "Money Forward Cloud Accounting MCP (developers.biz.moneyforward.com). Use this skill for ANY Money Forward Cloud Accounting MCP request — reading, creating, and updating data. Whenever a task involves Money Forward Cloud Accounting MCP, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Money Forward Cloud Accounting MCP"
  author: "OOMOL"
  version: "1.0.2"
  services: ["moneyforward_mcp"]
  icon: "https://static.oomol.com/logo/third-party/moneyforward_mcp.svg"
---

# Money Forward Cloud Accounting MCP

Operate **Money Forward Cloud Accounting MCP** through your OOMOL-connected account. This skill calls the `moneyforward_mcp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Money Forward Cloud Accounting MCP. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "moneyforward_mcp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "moneyforward_mcp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `current_office` — Get one office's name, type and accounting periods, newest first.
- `en_ja_dictionary` — Get Money Forward's English-to-Japanese glossary of accounting terms, for matching English wording to the Japanese names the other tools return.
- `get_accessible_offices` — List the offices this API key can use in Money Forward Cloud Accounting, with each office's number, name and accounting periods. Start here to find office_code; offices without Cloud Accounting are not listed.
- `get_accounts` — List the office's account items (勘定科目).
- `get_connected_accounts` — List the bank, card and other services connected to the office, with their account IDs.
- `get_departments` — List the office's departments (部門).
- `get_journal_by_id` — Get one journal entry by its ID.
- `get_journals` — List journal entries (仕訳) in a date range. Give start_date, end_date or both; results are paginated.
- `get_reports_transition_balance_sheet` — Get the month-by-month transition (推移表) balance sheet of a fiscal year. Zero-balance items are omitted.
- `get_reports_transition_profit_loss` — Get the month-by-month transition (推移表) profit and loss statement of a fiscal year. Zero-balance items are omitted.
- `get_reports_trial_balance_balance_sheet` — Get the trial balance (残高試算表) balance sheet for a fiscal year or a custom period. Zero-balance items are omitted.
- `get_reports_trial_balance_profit_loss` — Get the trial balance (残高試算表) profit and loss statement for a fiscal year or a custom period. Zero-balance items are omitted.
- `get_sub_accounts` — List the office's sub-accounts (補助科目), optionally for one account item.
- `get_taxes` — List the office's tax categories (税区分).
- `get_term_settings` — Get every fiscal-year setting of an office (dates, accounting and consumption-tax methods), newest first.
- `get_trade_partners` — List the office's business partners (取引先).
- `get_transactions` — List bank, card and other transactions (明細) collected from connected services, within a date range of at most 366 days.
- `list_tools` — List the tools the Money Forward Cloud Accounting MCP server exposes right now, with their live input schemas. Use it to spot server-side changes.
- `post_journals` — Create a journal entry (仕訳). Writes to the accounting ledger: confirm the office and content with the user first. Never retried automatically; when data.writeOutcome is outcome_unknown, check the ledger before trying again. [write]
- `post_trade_partners` — Create business partners (取引先). Writes to the accounting ledger: confirm the office and content with the user first. Never retried automatically; when data.writeOutcome is outcome_unknown, check the ledger before trying again. [write]
- `post_transaction_journalize` — Create a journal entry from one connected transaction (明細), booking it to the given account. Writes to the accounting ledger: confirm the office and content with the user first. Never retried automatically; when data.writeOutcome is outcome_unknown, check the ledger before trying again. [write]
- `post_transactions` — Add transactions (明細) to a connected service by hand. Writes to the accounting ledger: confirm the office and content with the user first. Never retried automatically; when data.writeOutcome is outcome_unknown, check the ledger before trying again. [write]
- `put_journals` — Replace a journal entry by its ID. Fields left out are overwritten, so send the complete entry. Writes to the accounting ledger: confirm the office and content with the user first. Never retried automatically; when data.writeOutcome is outcome_unknown, check the ledger before trying again. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Money Forward Cloud Accounting MCP state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Money Forward Cloud Accounting MCP is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/moneyforward_mcp
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Money Forward Cloud Accounting MCP homepage: https://developers.biz.moneyforward.com/mcp/
- API documentation: https://developers.biz.moneyforward.com/mcp/
