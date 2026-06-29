---
name: oo-jin10
description: "Jin10 (jin10.com). Use this skill for ANY Jin10 request — searching and reading data. Whenever a task involves Jin10, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Jin10"
  author: "OOMOL"
  version: "1.0.0"
  services: ["jin10"]
  icon: "https://static.oomol.com/logo/third-party/jin10.png"
---

# Jin10

Operate **Jin10** through your OOMOL-connected account. This skill calls the `jin10` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Jin10. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "jin10" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "jin10" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_kline` — Get minute-level K-line data for a supported Jin10 instrument code.
- `get_news` — Get the full details for one Jin10 news article by article ID.
- `get_quote` — Get a real-time Jin10 quote for a supported instrument code.
- `list_calendar` — Get Jin10 economic calendar items for the current natural week.
- `list_flash` — List the latest Jin10 flash news items with cursor pagination.
- `list_news` — List the latest Jin10 news articles with cursor pagination.
- `list_quote_codes` — List quote instrument codes supported by Jin10 from the `quote://codes` MCP resource.
- `search_flash` — Search Jin10 flash news by keyword. The MCP tool returns up to 150 items without pagination.
- `search_news` — Search Jin10 news articles by keyword with cursor pagination.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Jin10 state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Jin10 is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=jin10
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Jin10 homepage: https://www.jin10.com
