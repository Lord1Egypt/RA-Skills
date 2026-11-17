---
name: oo-fundzwatch
description: "FundzWatch (fundzwatch.ai). Use this skill for ANY FundzWatch request — reading, creating, and updating data. Whenever a task involves FundzWatch, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "FundzWatch"
  author: "OOMOL"
  version: "1.0.4"
  services: ["fundzwatch"]
  icon: "https://static.oomol.com/logo/third-party/fundzwatch.svg"
---

# FundzWatch

Operate **FundzWatch** through your OOMOL-connected account. This skill calls the `fundzwatch` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected FundzWatch. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "fundzwatch" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "fundzwatch" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_to_watchlist` — Add one or more company domains to the connected FundzWatch account's watchlist. Requires a FundzWatch API key. [write]
- `get_benefit_plans` — Get recently funded companies with benefit-plan filings, renewal timing, participant counts, and incumbent carrier evidence. No API key is required; anonymous results may be a limited preview.
- `get_brokers` — Search the FundzWatch benefits broker-of-record directory derived from Form 5500 Schedule A filings. No API key is required; Fundz attribution and licensing metadata is returned with the results.
- `get_events` — Get recent FundzWatch business events, including funding rounds, acquisitions, executive hires, contracts, and product launches. Requires a FundzWatch API key.
- `get_funded_and_hiring` — Get score-ranked companies with a verified recent funding round and live hiring evidence. No API key is required; anonymous results may be a limited preview.
- `get_lenders` — Search the FundzWatch UCC secured-party directory ranked by filing activity and lapsing-soon exposure. No API key is required; Fundz attribution and licensing metadata is returned with the results.
- `get_market_brief` — Get the current FundzWatch AI-generated strategic intelligence brief and its referenced companies. Requires a FundzWatch API key.
- `get_market_pulse` — Get the FundzWatch market activity overview with recent funding, acquisition, executive-move, contract, and product-launch aggregates. Requires a FundzWatch API key.
- `get_money_in_motion` — Get companies combining a recent executive move with recent funding, highlighting wealth and benefits money-in-motion moments. No API key is required; anonymous results may be a limited preview.
- `get_renewal_radar` — Get companies whose active UCC-1 liens approach their lapse dates, identifying potential refinancing windows. No API key is required; anonymous results may be a limited preview.
- `get_scored_leads` — Get FundzWatch leads scored against the connected account's ideal customer profile, including buyer intent and outreach guidance. Requires a FundzWatch API key.
- `get_stacked_borrowers` — Get companies with active secured debt from multiple distinct lenders and recent UCC activity. No API key is required; anonymous results may be a limited preview.
- `get_usage` — Get the connected FundzWatch API key's current tier, usage counters, and limits. Requires a FundzWatch API key.
- `get_watchlist` — List the companies tracked by the connected FundzWatch account. Requires a FundzWatch API key.
- `get_watchlist_events` — Get recent business events for companies on the connected FundzWatch account's watchlist. Requires a FundzWatch API key.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change FundzWatch state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — FundzWatch is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/fundzwatch
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- FundzWatch homepage: https://fundzwatch.ai/
- API documentation: https://fundzwatch.ai/docs
