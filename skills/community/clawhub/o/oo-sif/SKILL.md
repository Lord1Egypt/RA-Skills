---
name: oo-sif
description: "Sif (sif.com). Use this skill for ANY Sif request — searching and reading data. Whenever a task involves Sif, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Sif"
  author: "OOMOL"
  version: "1.0.4"
  services: ["sif"]
  icon: "https://static.oomol.com/logo/third-party/sif.png"
---

# Sif

Operate **Sif** through your OOMOL-connected account. This skill calls the `sif` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Sif. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sif" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sif" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `call_tool` — Call a current Sif MCP Amazon analysis tool with JSON arguments after discovering its live input schema.
- `list_tools` — Discover the current Sif Amazon analysis tools and their live input schemas before choosing a tool to call.
- `market_discover_competitors` — Analyze and filter a keyword's Top-100 competitor pool by price, review threshold, sales, and competitive posture. Costs 3 Sif points.
- `market_get_asin_aba_footprint` — Reverse-map an ASIN to search terms where it occupies an ABA Top-3 position. Costs 2 Sif points.
- `market_get_asin_keyword_signals` — Analyze an ASIN's keyword traffic contribution, organic and paid dependence, rank stability, and health signals. Costs 3 Sif points.
- `market_get_asin_profile` — Get product-positioning profiles such as price, rating, reviews, BSR, brand, listing age, variants, and dimensions for up to 20 ASINs. Costs 2 Sif points per input ASIN.
- `market_get_keyword_competition` — Analyze a keyword's traffic-share leaders, ABA Top-3 concentration, market accessibility, and optional ASIN competitive position. Costs 2 Sif points.
- `market_get_keyword_demand` — Diagnose demand lifecycle and seasonal timing for up to 20 keywords. Costs 2 Sif points.
- `market_get_keyword_history` — Get raw historical ABA search volume, rank, and Top-3 click and conversion concentration for up to 10 keywords. Costs 1 Sif point.
- `market_get_keyword_root_competitors` — Discover the leading ASIN competitors across a keyword root using ABA buyer click behavior. Costs 2 Sif points.
- `market_get_keyword_root_trend` — Compare exact-keyword demand with aggregate keyword-root demand to assess market size and demand concentration. Costs 3 Sif points.
- `market_screen_keyword_opportunities` — Rank keyword-root variants by demand and click-concentration opportunity signals. Costs 3 Sif points.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Sif state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Sif is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/sif
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Sif homepage: https://www.sif.com
- API documentation: https://blog.sif.com/article/mcp-install/Sif-MCP%E5%AE%89%E8%A3%85%E6%96%87%E6%A1%A3
