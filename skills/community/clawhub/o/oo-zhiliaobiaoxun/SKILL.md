---
name: oo-zhiliaobiaoxun
description: "Zhiliao Biaoxun (zhiliaobiaoxun.com). Use this skill for ANY Zhiliao Biaoxun request — searching and reading data. Whenever a task involves Zhiliao Biaoxun, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Zhiliao Biaoxun"
  author: "OOMOL"
  version: "1.0.2"
  services: ["zhiliaobiaoxun"]
  icon: "https://static.oomol.com/logo/third-party/zhiliaobiaoxun.png"
---

# Zhiliao Biaoxun

Operate **Zhiliao Biaoxun** through your OOMOL-connected account. This skill calls the `zhiliaobiaoxun` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Zhiliao Biaoxun. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "zhiliaobiaoxun" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "zhiliaobiaoxun" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_account_balance` — Read available credits and cumulative charged and consumed credits for the connected account. This endpoint does not consume credits.
- `get_bid_detail` — Read a procurement notice with its full text and attachment links. Supply a notice URL, unique key, or notice ID. Charges provider credits; attachments are returned as URLs.
- `get_bid_timeline` — Retrieve notices for every stage of the same procurement project, ordered by publication time ascending. Supply a notice URL or a notice ID with its type. Charges provider credits.
- `search_bids` — Search Chinese tender and award notices by keywords, region, publication date, or amount. Returns one page per call and charges provider credits. Increase page to continue.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Zhiliao Biaoxun state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Zhiliao Biaoxun is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/zhiliaobiaoxun
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Zhiliao Biaoxun homepage: https://www.zhiliaobiaoxun.com/
- API documentation: https://ai.zhiliaobiaoxun.com/docs/api
