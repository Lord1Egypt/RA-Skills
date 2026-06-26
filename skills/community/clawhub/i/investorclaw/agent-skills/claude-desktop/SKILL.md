---
name: investorclaw
description: Deterministic-first portfolio analyzer for Claude Desktop via MCP-HTTP at localhost:18090. Holdings, performance, Sharpe + Sortino, FRED yields, bond duration, scenario rebalancing.
homepage: https://github.com/argonautsystems/InvestorClaw
user-invocable: true
metadata: {"license":"MIT-0","version":"4.7.7","runtime":"claude-desktop","image":"ghcr.io/argonautsystems/ic-engine:4.7.7-cpu","mcp-endpoint":"http://localhost:18090/mcp"}
---

<!--
SPDX-License-Identifier: MIT-0
Copyright 2026 InvestorClaw Contributors

This SKILL.md is MIT-0-licensed. The InvestorClaw service it connects to is
Apache 2.0. See ../../LICENSE-MIT-0 for the full MIT text.
-->

# InvestorClaw — Claude Desktop Reference

> Powered by [InvestorClaw](https://investorclaw.app) (Apache 2.0).
> This reference doc is MIT-0-licensed; the underlying service is Apache 2.0.

## What this is

[InvestorClaw](https://investorclaw.app) is a containerized, deterministic
portfolio analysis service. It runs on your machine as two Docker
containers (a Rust memory server and a Python analysis engine) and
exposes its capabilities to Claude Desktop over MCP-HTTP.

Claude Desktop has no plugin system — instead, it connects to MCP servers
declared in `claude_desktop_config.json`. Once you run
`docker compose up -d` and add two short blocks to that config file
(see `INSTALL.md`), Claude Desktop gains an entire portfolio-analysis
toolkit that you can invoke just by chatting.

There is no marketplace step. There is no plugin to install. The
service is the substrate; Claude Desktop is the interface.

## Tools that become available after install

Once both MCP servers are wired up and Claude Desktop has been fully
quit and relaunched, the model gains two new tool namespaces.

### Portfolio analysis (`investorclaw.*`)

| Tool | What it does |
|---|---|
| `investorclaw.portfolio_ask` | Natural-language question routed through the deterministic engine |
| `investorclaw.portfolio_holdings` | Current snapshot of positions, values, and weights |
| `investorclaw.portfolio_performance` | Sharpe, volatility, top/bottom performers, max drawdown |
| `investorclaw.portfolio_bonds` | Bond analytics — YTM, duration, FRED yield curve |
| `investorclaw.portfolio_analyst` | Analyst consensus ratings per holding |
| `investorclaw.portfolio_news` | News correlation for held positions |
| `investorclaw.portfolio_lookup` | Ticker / account lookup |
| `investorclaw.portfolio_optimize` | Modern Portfolio Theory (Sharpe / min-vol) |
| `investorclaw.portfolio_rebalance` | Current vs. target with tax impact |
| `investorclaw.portfolio_scenario` | What-if scenarios (rate moves, drawdowns) |
| `investorclaw.portfolio_cashflow` | Projected dividends and bond coupons |
| `investorclaw.portfolio_peer` | Peer comparison vs. benchmark |
| `investorclaw.portfolio_setup` | Auto-discover portfolio files in `/data/portfolios/` |
| `investorclaw.portfolio_refresh` | Refresh market data without re-uploading files |
| `investorclaw.portfolio_guardrails` | View / configure educational-only guardrails |

### Memory (`mnemos.*`)

| Tool | What it does |
|---|---|
| `mnemos.search_memories` | Full-text + semantic search across saved observations |
| `mnemos.create_memory` | Record an observation about preferences, prior questions, or context |
| `mnemos.list_memories` | Browse memories by category or date |

## How to use it in Claude Desktop

You don't invoke tools by name — you just talk to Claude. Examples:

| Intent | Phrasing |
|---|---|
| Holdings | "What's in my portfolio?" • "Show me my positions" |
| Performance | "How am I doing this year?" • "What's my Sharpe ratio?" |
| Bonds | "Show me my bond exposure and yield-to-maturity" |
| Allocation | "What's my sector exposure?" |
| Optimization | "Help me rebalance to a 60/40 target" |
| Market data | "What's the current price of NVDA?" |
| News | "Today's news on my holdings" |
| Reports | "Generate today's EOD report" • "Prepare a brief for my advisor" |
| Stress test | "What if rates rise 100 bps?" |
| Memory | "Remember that I treat BABA as a sentimental hold" • "What did we discuss about my bond ladder last time?" |

Claude routes the request to the right tool, surfaces the structured
result, and decorates it with narrative context. The first call after a
cold cache may take 30–60 seconds while the deterministic pipeline builds
the signed envelope; subsequent calls reuse the cache.

## Recommended model split

Claude Desktop uses the agent's own LLM — no external API key required.

- **Narrative**: Haiku 4.5 — fast, cheap, ~10× lower output cost than
  Sonnet. With a clean signed envelope, narrative synthesis is mostly
  transcription, so the cheap model is sufficient.
- **Validator**: Sonnet 4.6 (default) or Opus 4.7 (escalation) — gates
  the Haiku output for fabrication, mis-quoted numbers, and training-leak
  drift. Validator output is short (~1 K tokens), so the smart-model bill
  stays low.

Cost-shaped: cheap model on the long output, smart model on the short
safety check.

## Important behaviors

- **Deterministic by design.** Portfolio math is not generated by an
  LLM. The Python engine in the ic-engine container computes every
  number. Claude reports those numbers; it does not invent them. If
  Claude ever appears to fabricate a holding or a return, that's a bug
  — file it.
- **Educational only — never investment advice.** All outputs include
  a disclaimer envelope. Claude will echo it when summarizing.
- **Localhost-only by default.** Both MCP servers bind to `127.0.0.1`.
  Nothing leaves your machine unless you explicitly enable a remote
  deployment via the dashboard.
- **What Claude sees vs what stays local.** Claude Desktop's
  transcript receives the agent's tool-call inputs and outputs — that
  includes the user's question, the structured `ic_result` envelope
  (ticker symbols, asset-class breakdowns, computed metrics), and
  the narrator's prose answer. **It does NOT receive raw broker CSVs**
  — those stay on your local filesystem in the bind-mounted
  `./portfolios/` directory. Account numbers and SSNs are scrubbed at
  ingest. See [PRIVACY.md](../../PRIVACY.md) for the full data-flow
  matrix.
- **Unknown CSV format?** The engine returns a structured error with
  detected columns. Claude will direct you to the column-mapping
  wizard at `http://localhost:18092/portfolios/map` rather than
  guessing.

## What this does NOT do

- Does not place trades or move money
- Does not give personalized investment advice
- Does not connect directly to broker accounts (you upload CSV / XLS / PDF)
- Does not require an internet connection for portfolio math (only for
  market-data refresh, which gracefully degrades without API keys)

## Install

Claude Desktop connects to InvestorClaw via MCP servers — there is no plugin to install from a marketplace. The service runs locally via Docker Compose.

**Start the service:**

```bash
git clone https://github.com/mnemos-os/mnemos-ic-runtime.git ~/.investorclaw
cd ~/.investorclaw
mkdir -p portfolios
docker compose up -d
```

Then add the MCP server blocks to `claude_desktop_config.json` and restart Claude Desktop. See `INSTALL.md` in this directory for the exact config snippet.

**OpenClaw / ZeroClaw / Hermes users:** install via ClawHub:

```bash
clawhub install investorclaw
```

## Where to go next

- **`INSTALL.md`** in this directory — step-by-step install
  instructions including the exact Claude Desktop config edit.
- **`config-snippet.json`** in this directory — the JSON block to merge
  into `claude_desktop_config.json`.
- **Dashboard** at `http://localhost:18092` once running — upload
  portfolio files, configure provider keys, manage memory retention,
  inspect MCP traffic.

## Reporting issues

This SKILL.md describes the InvestorClaw service. If a tool returns an
unexpected result, the issue is in the service
([`argonautsystems/InvestorClaw`](https://github.com/argonautsystems/InvestorClaw),
Apache 2.0) or in the runtime bridge
([`mnemos-os/mnemos-ic-runtime`](https://github.com/mnemos-os/mnemos-ic-runtime),
Apache 2.0), not in this MIT-0-licensed reference doc.
