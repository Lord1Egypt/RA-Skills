<!--
SPDX-License-Identifier: MIT-0
Copyright 2026 InvestorClaw Contributors

This DESCRIPTION.md is MIT-0-licensed. It is the short skill-catalog
entry hermes 0.12+ surfaces in `skills_list` / `skill_view`. The
underlying InvestorClaw service is Apache 2.0.
-->

# InvestorClaw

Containerized portfolio analysis for hermes. Two local MCP-HTTP
servers (`investorclaw` on :8090, `mnemos` on :5002) expose
deterministic portfolio analytics and a persistent memory layer as
first-class function-callable tools — no skill-bundle indirection,
no meta-tool roundabouts. Upload a broker CSV / XLS / PDF at the
local dashboard, then ask portfolio questions in `hermes chat` and
the LLM routes natively to the right analyzer.

## When to use this skill

- The user asks about their portfolio, holdings, allocation, or
  account balances.
- The user asks about performance: returns, Sharpe ratio,
  volatility, drawdown, top / bottom performers.
- The user asks about bonds: yield-to-maturity, duration, ladder,
  cashflow calendar, FRED yield-curve comparisons.
- The user asks about analyst ratings, news sentiment, or recent
  headlines for held positions.
- The user wants to rebalance, optimize, or run scenario / what-if
  analysis on holdings.
- The user asks "what changed?" — combine `mnemos.search_memories`
  with `investorclaw.portfolio_holdings` to diff against prior
  observations.
- The user attaches a broker CSV / XLS / PDF and wants it analyzed.

## When NOT to use this skill

- General-purpose chat unrelated to investing.
- Code editing, software engineering, or shell tasks (use hermes'
  built-in `terminal`, `skill_*`, browser tools).
- Trade execution, money movement, or any action against a real
  brokerage account — InvestorClaw is read-only and educational.
- Real-time market quotes for tickers the user does NOT hold —
  InvestorClaw analyzes the user's portfolio, not generic market
  data.
- Tax / legal / fiduciary advice — outputs are educational only.

## Available MCP tools

**`investorclaw.*`** (port 8090):

- `investorclaw.portfolio_ask` — natural-language portfolio Q
- `investorclaw.portfolio_holdings` — positions / values / weights
- `investorclaw.portfolio_performance` — returns + risk metrics
- `investorclaw.portfolio_bonds` — bond analytics (YTM, duration)
- `investorclaw.portfolio_analyst` — analyst ratings
- `investorclaw.portfolio_news` — news correlation per holding
- `investorclaw.portfolio_lookup` — ticker / account lookup
- `investorclaw.portfolio_optimize` — Sharpe / min-vol optimization
- `investorclaw.portfolio_rebalance` — current vs target + tax impact
- `investorclaw.portfolio_scenario` — what-if scenario analysis
- `investorclaw.portfolio_cashflow` — projected bond cashflows
- `investorclaw.portfolio_peer` — peer / benchmark comparison
- `investorclaw.portfolio_setup` — auto-discover portfolio files
- `investorclaw.portfolio_refresh` — refresh market data
- `investorclaw.portfolio_guardrails` — guardrails configuration

**`mnemos.*`** (port 5002):

- `mnemos.search_memories` — full-text + semantic memory search
- `mnemos.create_memory` — record observations / user preferences
- `mnemos.list_memories` — browse by category / date

## Prerequisite — service must be running

These MCP tools only appear in hermes' catalog if the local
InvestorClaw service is up. Verify with:

```bash
curl -fsS http://localhost:18090/healthz   # ic-engine
curl -fsS http://localhost:5002/healthz   # mnemos-rs
```

If either fails: `cd ~/.investorclaw && docker compose up -d`. Full
setup in `INSTALL.md`.

## License attribution

Skill files (this directory): MIT. Underlying service: Apache 2.0.
