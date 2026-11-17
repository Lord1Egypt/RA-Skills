---
name: oo-wisburg
description: "Wisburg (wisburg.com). Use this skill for ANY Wisburg request — searching and reading data. Whenever a task involves Wisburg, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Wisburg"
  author: "OOMOL"
  version: "1.0.2"
  services: ["wisburg"]
  icon: "https://static.oomol.com/logo/third-party/wisburg.svg"
---

# Wisburg

Operate **Wisburg** through your OOMOL-connected account. This skill calls the `wisburg` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Wisburg. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "wisburg" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "wisburg" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_am_report` — Get one Wisburg asset-management research report (资管报告) by report ID, including the download URL and Markdown summary.
- `get_archive` — Get one Wisburg literature research report (文献) by report ID, including the download URL and Markdown summary.
- `get_article` — Get one Wisburg column article (文章) by article ID, including the HTML body.
- `get_company_report` — Get one Wisburg single-company research report (企业研究) by report ID, including the download URL and Markdown summary.
- `get_earnings_call` — Get one Wisburg earnings call minutes document (电话会纪要) by ID, including the download URL and Markdown summary.
- `get_mikko_log` — Get one Wisburg Mikko log entry (Mikko 日志) by log ID. Returns the same fields as the list.
- `get_report` — Get one Wisburg research note (研报笔记) by report ID, including the Markdown summary.
- `list_am_reports` — List Wisburg asset-management research reports (资管报告) with cursor pagination, keyword search, and time filters.
- `list_archives` — List Wisburg literature research reports (文献) with cursor pagination, keyword search, and time filters.
- `list_articles` — List Wisburg column articles (文章) with cursor pagination, keyword search, and time filters. Mikko logs are not included; use list_mikko_logs for those.
- `list_company_reports` — List Wisburg single-company research reports (企业研究) with cursor pagination, keyword search, and time filters.
- `list_earnings_calls` — List Wisburg earnings call minutes (电话会纪要) with cursor pagination, keyword search, and time filters.
- `list_feed` — List the Wisburg news feed (资讯流) with cursor pagination, keyword search, and time filters. Feed items carry the full Markdown body in `content`.
- `list_images` — List the Wisburg image feed (图片流) with cursor pagination, keyword search, and time filters.
- `list_market_daily` — List the Wisburg AI market daily (AI 市场日报) with cursor pagination, keyword search, and time filters.
- `list_mikko_logs` — List Wisburg Mikko log entries (Mikko 日志), newest first. Each entry is a short Markdown note; the list already returns the full content.
- `list_reports` — List Wisburg research notes (研报笔记) with cursor pagination, keyword search, and time filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Wisburg state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Wisburg is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/wisburg
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Wisburg homepage: https://www.wisburg.com
- API documentation: https://open-docs.wisburg.com/docs/getting-started/first-call
