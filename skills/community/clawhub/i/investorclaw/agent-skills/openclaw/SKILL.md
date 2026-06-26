---
name: investorclaw
description: Deterministic-first portfolio analyzer for OpenClaw via MCP-HTTP at localhost:18090. Holdings, performance, Sharpe + Sortino, FRED yields, bond duration, scenario rebalancing.
homepage: https://github.com/argonautsystems/InvestorClaw
user-invocable: true
metadata: {"license":"MIT-0","version":"4.7.7","runtime":"openclaw","image":"ghcr.io/argonautsystems/ic-engine:4.7.7-cpu","mcp-endpoint":"http://localhost:18090/mcp"}
---

<!--
SPDX-License-Identifier: MIT-0
Copyright 2026 InvestorClaw Contributors

This SKILL.md is MIT-0-licensed. The InvestorClaw service it connects to
is Apache 2.0. See the InvestorClaw repository for that license.
-->

# InvestorClaw — Skill (openclaw runtime)

> Powered by [InvestorClaw](https://investorclaw.app) (Apache 2.0).
> This skill file is MIT-0-licensed; the underlying service is Apache 2.0.

## What this is

InvestorClaw is a containerized portfolio-analysis service exposed to
openclaw as **two MCP-HTTP servers**:

- `investorclaw` — portfolio analysis tools at `http://localhost:18090/mcp`
- `mnemos` — memory + knowledge graph at `http://localhost:5002/mcp`

Both run inside a Docker compose stack on the user's machine
(`docker compose up -d` is the entire service install). openclaw connects
to them as native MCP servers via its `mcp.servers` config block —
no plugin manifest, no `dist/index.js`, no npm install, no skill
bootstrap files.

If openclaw runs in a container itself, the two MCP URLs reach the host's
loopback through the compose bridge network or `host.docker.internal`,
depending on how the openclaw container is launched. See `INSTALL.md`.

## Tool surface

When the service is running, openclaw's tool catalog gains:

### Portfolio analysis (`investorclaw.*`)

- `investorclaw.portfolio_ask` — natural-language portfolio question
  routed through the deterministic engine
- `investorclaw.portfolio_holdings` — current snapshot of positions,
  values, weights
- `investorclaw.portfolio_performance` — Sharpe, volatility, top/bottom
  performers, max drawdown
- `investorclaw.portfolio_bonds` — bond analytics (YTM, duration, FRED
  yield curve)
- `investorclaw.portfolio_analyst` — analyst ratings per holding
- `investorclaw.portfolio_news` — news correlation for held positions
- `investorclaw.portfolio_lookup` — ticker / account lookup
- `investorclaw.portfolio_optimize` — Sharpe / min-vol optimization
- `investorclaw.portfolio_rebalance` — current vs target with tax impact
- `investorclaw.portfolio_scenario` — what-if scenarios on holdings
- `investorclaw.portfolio_cashflow` — projected cashflow from bonds
- `investorclaw.portfolio_peer` — peer comparison vs benchmark
- `investorclaw.portfolio_setup` — auto-discover portfolio files in
  `/data/portfolios/`
- `investorclaw.portfolio_refresh` — refresh market data without
  re-uploading files
- `investorclaw.portfolio_guardrails` — view educational-only guardrails

### Memory (`mnemos.*`)

- `mnemos.search_memories` — full-text + semantic search across
  remembered observations
- `mnemos.create_memory` — record an observation about the user's
  preferences, prior questions, or current investing context
- `mnemos.list_memories` — browse by category / date

## How users interact with it

Users ask portfolio questions in openclaw chat. The LLM sees the MCP
tools in its function-calling schema and routes the question to the
right tool automatically. Examples:

- "What's in my portfolio?" → `investorclaw.portfolio_holdings`
- "How am I doing this year?" → `investorclaw.portfolio_performance`
- "What did I tell you about BABA last month?" → `mnemos.search_memories`

| Intent | Phrasing |
|---|---|
| Holdings | "What's in my portfolio?" • "Show me my positions" |
| Performance | "How am I doing this year?" • "What's my Sharpe ratio?" |
| Bonds | "Show me my bond exposure and yield-to-maturity" |
| Allocation | "What's my sector exposure?" |
| Optimization | "Help me rebalance to a 60/40 target" |
| Market data | "What's the current price of NVDA?" |
| News | "Today's news on my holdings" |
| Reports | "Generate today's EOD report" • "Prepare an advisor brief" |

The first call after a cold cache may take 30–60 seconds while the
deterministic pipeline builds the signed envelope; subsequent calls reuse
the cache.

A typical flow:

1. User asks: *"What changed since last review?"*
2. openclaw's LLM calls `mnemos.search_memories` for prior portfolio
   context.
3. LLM calls `investorclaw.portfolio_holdings` for the current snapshot.
4. LLM compares the two and synthesizes a narrative.
5. LLM calls `mnemos.create_memory` to record salient observations from
   the review.

## Recommended narrative model

openclaw's chat completion goes through whichever provider is configured
in `models.providers.<name>` of `~/.openclaw/openclaw.json`. **Anthropic
on openclaw — paid path only since 2026-04-04**: routing OAuth-
subscription tokens to a claws-agent violates Anthropic's ToS per their
Apr 3 announcement. To use Anthropic models you need either (a) the
discounted "extra usage bundle" add-on for your subscription, or (b) a
direct Anthropic API key. Even with paid credits, Anthropic isn't
cost-competitive with Together for InvestorClaw narrative work; we
don't deploy Anthropic on our own fleet for openclaw.

Recommended:

- **Default narrative** — Together AI `google/gemma-4-31B-it` — serverless
  tier, ~100 tok/s, ~$0.0008 / 1 K tokens, fleet default. This is what the
  InvestorClaw container expects via `INVESTORCLAW_NARRATIVE_MODEL`.
- **Higher-quality alternative** — Together AI `MiniMaxAI/MiniMax-M2` —
  larger context, but moved off Together's serverless tier 2026-05;
  requires a paid dedicated endpoint.
- **Local-only / offline** — Ollama `gemma4:e4b` on host — zero cloud
  cost, GPU-bound, no key required.

Set `TOGETHER_API_KEY` in the InvestorClaw container's
`portfolios/keys.env` (or via `portfolio_keys_set`) so the engine can
synthesize narratives directly. openclaw's own model config is a
separate concern.

After delivering analysis, the LLM should record only non-obvious
observations the user might want next time — not every detail, just the
ones that would be hard to recover from re-reading the data.

## Important behaviors

- **The investorclaw tools are deterministic at the data layer.** Each
  response includes a structured `ic_result` envelope plus a narrative
  text body. Trust the structured envelope — it is the source of truth.
  The narrative is decoration. If a portfolio file format isn't
  recognized, the tool returns a structured error with detected columns;
  surface that error and direct the user to the dashboard's column-mapping
  wizard at `http://localhost:18092/portfolios/map`.

- **Educational only — never investment advice.** All outputs include
  the disclaimer envelope. Echo it when summarizing for the user. Do not
  recommend buying, selling, or holding specific securities.

- **The MCP servers run on loopback by default.** `localhost:18090` and
  `localhost:5002`. If the user deploys remotely (Tailscale VM, cloud
  host), the URLs change but the tool surface is identical.

- **openclaw's own LLM provider config is separate.** openclaw routes
  *its* chat completions through `models.providers.<name>` in
  `~/.openclaw/openclaw.json` (Together, OpenAI, Ollama, etc.). That is
  unrelated to InvestorClaw's optional narrative tier, which is configured
  inside the InvestorClaw dashboard at `http://localhost:18092/`.

## v4.0 vs v2.x — what's different on openclaw

v4.0 eliminates the v2.x openclaw install friction:

- **No** `openclaw.plugin.json` manifest (there is no plugin)
- **No** `dist/index.js` (there is no plugin shim to compile)
- **No** install step inside an openclaw container
- **No** workspace bootstrap files (`BOOTSTRAP.md` / `IDENTITY.md` /
  `USER.md`) to seed
- **No** schema-validation daemon to fight when writing provider config
  for the plugin

The integration is just two MCP server URLs. openclaw's existing native
MCP support handles the rest.

## What this skill does NOT do

- Does not manage money or execute trades
- Does not give investment advice
- Does not access user accounts or move funds
- Educational outputs only

## Install

**OpenClaw / ZeroClaw / Hermes (ClawHub):**

```bash
clawhub install investorclaw
```

**Claude Code / Claude Desktop:**

```
/plugin marketplace add argonautsystems/InvestorClaw
/plugin install investorclaw
```

See `INSTALL.md` in this directory for manual install steps.

## Reporting issues

This SKILL.md describes how openclaw connects to the InvestorClaw
service. If a tool returns an unexpected result, the issue is in the
service (Apache 2.0 — `mnemos-os/mnemos-ic-runtime` and
`argonautsystems/InvestorClaw`), not in this file. If openclaw fails to register
the MCP servers, see `INSTALL.md` in this directory — in particular the
note about always using the validated `openclaw mcp set` /
`openclaw config patch` CLI rather than editing `openclaw.json` by hand.
