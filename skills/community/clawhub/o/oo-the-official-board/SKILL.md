---
name: oo-the-official-board
description: "The Official Board (theofficialboard.com). Use this skill for ANY The Official Board request — searching and reading data. Whenever a task involves The Official Board, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "The Official Board"
  author: "OOMOL"
  version: "1.0.4"
  services: ["the_official_board"]
  icon: "https://static.oomol.com/logo/third-party/the_official_board.png"
---

# The Official Board

Operate **The Official Board** through your OOMOL-connected account. This skill calls the `the_official_board` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected The Official Board. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "the_official_board" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "the_official_board" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `find_executive` — Find executives by an exact email address or LinkedIn profile URL.
- `get_company_org_chart` — Retrieve a company organizational chart and its executives in structured JSON.
- `get_executive_biography` — Retrieve detailed biography information for an executive.
- `list_direct_colleagues` — List the direct colleagues in an executive's organizational environment.
- `list_recent_org_chart_news` — List the main organizational chart changes for a company from the past 12 months.
- `list_watchlist_changes` — List recently modified organizational charts from the connected user's watchlist.
- `search_companies` — Find company organizational chart identifiers by company name.
- `search_executives` — Search executives by first name, last name, or full name.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change The Official Board state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — The Official Board is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/the_official_board
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- The Official Board homepage: https://www.theofficialboard.com/
- API documentation: https://rest.theofficialboard.com/rest/api/doc/
