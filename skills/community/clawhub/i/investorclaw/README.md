<p align="center">
  <picture>
    <source srcset="assets/investorclaw-logo.webp" type="image/webp">
    <img src="assets/investorclaw-logo.jpg" alt="InvestorClaw" width="192">
  </picture>
</p>

# InvestorClaw

> Deterministic-first portfolio analysis. Real money math, no LLM math.

Portfolio analysis and market intelligence for any MCP-capable agent.

v4.1.34 | Apache 2.0 + MIT-0 | Educational Use Only

InvestorClaw v4.x is a containerized portfolio analyzer that runs as a
Docker Compose stack and exposes its tools over MCP-HTTP at
`localhost:18090`. Any MCP-capable agent — Claude Code, Claude Desktop,
openclaw, zeroclaw, hermes — connects as a thin client. No Python
install on the agent side, no per-runtime plugin shim, no
language-specific bootstrap.

## Features

InvestorClaw analyzes multi-account portfolios with deterministic
Python computation. The agent presents the engine narrator's
HMAC-signed envelope answer; it does not guess financial metrics.

- Holdings snapshots for what you own and where you own it
- Performance metrics for returns, Sharpe + Sortino ratios, max
  drawdown, beta, value-at-risk
- Bond analytics for yield-to-maturity, duration, credit quality, and
  ladders
- Analyst consensus and price targets on portfolio holdings
- Today's news on holdings and market-wide topics (per-symbol +
  general / forex / crypto / merger categories)
- Portfolio synthesis, optimization, target allocation, drift, scenarios
- Direct ingestion from CSV, XLS, XLSX, PDF, and broker screenshots
- **End-of-day report generation** for daily summaries
- **Stonkmode** — narrated commentary mode with rotating fictional
  cable-finance personalities (Dr. Stonk, Mission Control, 30+ personas)
- Educational guardrails; no investment advice

## Install

### OpenClaw / ZeroClaw / Hermes (ClawHub)

```bash
clawhub install investorclaw
```

ClawHub handles the Docker Compose pull, MCP server registration, and
port wiring automatically.

### Claude Code / Claude Desktop

```
/plugin marketplace add argonautsystems/InvestorClaw
/plugin install investorclaw
```

Claude Code and Claude Desktop install the plugin directly from this
repo. They use the same skill bundle and the same container-first
runtime as OpenClaw, ZeroClaw, and Hermes. See
[docs/GETTING_STARTED.md](../docs/GETTING_STARTED.md) for the full
container-first setup.

### Manual (Docker Compose, any agent)

## Quick Start

```bash
git clone https://github.com/mnemos-os/mnemos-ic-runtime.git ~/.investorclaw
cd ~/.investorclaw
mkdir -p portfolios     # IMPORTANT: pre-create so docker doesn't auto-create as root
docker compose up -d    # uses the bundled compose.yml
```

That's it. The compose pulls
`ghcr.io/argonautsystems/ic-engine:4.7.7-cpu` (publicly hosted, no
auth) and runs it on `localhost:18090` (MCP + REST) and
`localhost:18092` (dashboard).

After the container reports `init_state: ready`, ask your first
question through your agent:

```text
What's in my portfolio?
```

Connect your agent — see [SKILL.md](SKILL.md) for per-runtime config
blocks (Claude Code, Claude Desktop, openclaw, zeroclaw, hermes).

## Prepare Your Portfolio

Export holdings from your broker. CSV offers the highest compatibility.

- Schwab: Accounts → Positions → Export CSV
- Fidelity: NetBenefits → Investments → Download CSV
- Vanguard: My Accounts → Download Holdings
- UBS: Wealth Management → Holdings → Export
- ETrade: Portfolio → Holdings → Download
- Robinhood: Account → Statements → CSV

Also supported: XLS / XLSX, PDF broker statements, and screenshots of
broker positions pages. Drop the file into the bind-mounted
`./portfolios/` directory under your compose project, or attach files
directly in your agent chat — the agent stages them automatically when
needed and asks the original question through `portfolio_ask`.

## Run Analysis

Ask in natural language. Your agent will route through `portfolio_ask`.

```text
What's in my portfolio?
How am I doing this year?
Show me my bond exposure and yield-to-maturity.
What's my Sharpe ratio?
What's my sector exposure?
Help me rebalance to a 60/40 target.
What is the current price of NVDA?
Today's news on my holdings.
```

### End-of-day report

```text
Generate today's EOD report.
```

The engine produces a daily summary covering holdings, performance,
bonds, analyst consensus, news, cashflow projections, and synthesis.
Reports land in `./reports/YYYY-MM-DD/` on the host. Send the report
to your advisor, archive it, or pass it back to the agent for
follow-up questions.

### Stonkmode (narrated commentary)

Stonkmode wraps portfolio output in commentary from a randomly-selected
pair of fictional cable-finance TV personalities (a "lead" and a
"foil"). The deterministic analysis runs unchanged — only the narrator
voice changes.

```text
Switch to stonkmode.
What's in my portfolio?
```

The dashboard at `localhost:18092` exposes a `--stonkmode on/off`
toggle, a Mission Control side panel with Dr. Stonk avatars (30+
personas, WebP-embedded for offline use), a soundboard, and a
Captain's Log. State persists in `~/.investorclaw/stonkmode.json`.

### Fresh data

Force a fresh pipeline run when news, prices, or portfolio files may
have moved:

```text
Refresh my portfolio.
```

## Available MCP Tools (13 Total)

| Tool | Purpose |
|---|---|
| **`portfolio_ask`** | **Primary tool — every portfolio question. Data is auto-loaded; just ask.** |
| `portfolio_initialize_status` | Poll before first ask: returns init `state` + per-stage progress |
| `portfolio_initialize` | Force a manual bootstrap (setup → refresh → seed ask) |
| `portfolio_holdings` | Holdings snapshot (advanced; `portfolio_ask` covers this) |
| `portfolio_refresh` | Force fresh data pull (auto-refresh runs on every ask) |
| `portfolio_setup` | Auto-discover portfolio files in the configured directory |
| `portfolio_keys_status` | Report which API keys are currently configured |
| `portfolio_keys_set` | Set one or more API keys (allowlisted) |
| `portfolio_keys_delete` | Delete a single configured API key by name |
| `portfolio_response_get` | Retrieve a stored portfolio response by run_id |
| `portfolio_response_list` | List recent stored responses |
| `portfolio_response_delete` | Permanently delete a stored response |

All 13 tools also have plain-HTTP REST endpoints at
`http://127.0.0.1:18090/api/portfolio/*` — useful when MCP integration
is flaky or you want to drive the engine from a shell.

## Dashboard / Web Portal

The dashboard runs at `http://localhost:18092` and is the human-facing
surface — separate from the MCP-HTTP agent surface at port 18090.

### 17 tabs

| Tab | What it shows |
|---|---|
| **Overview** | Portfolio summary + Regenerate sweep button |
| **Holdings** | Positions, values, weights, accounts |
| **Performance** | Returns, Sharpe, Sortino, max drawdown, beta, VaR |
| **WhatChanged** | Delta snapshot vs. prior run |
| **Scenarios** | Rate-shock, drawdown, and correlation-break what-if |
| **Bonds** | YTM, duration, convexity, FRED yield-curve overlay |
| **Optimize** | MPT: Sharpe-max, min-vol, target-return frontiers |
| **Cashflow** | Projected dividends and bond coupons |
| **Peer** | Peer and benchmark comparison |
| **Analyst** | Analyst consensus ratings per holding |
| **News** | News correlation for held positions |
| **Markets** | Market-wide news and macro data |
| **Lookup** | Ticker / account lookup |
| **Synthesis** | LLM-synthesized portfolio narrative |
| **Reports** | Browse and download EOD and advisor reports |
| **Settings** | API keys, portfolio upload form, preferences |
| **About** | Version, license, attribution |

All 30 natural-language queries in the agentic COBOL test suite map to
one of these 17 tabs — the tab coverage is complete.

### Regenerate button

The **Regenerate** button on the Overview tab fires a background sweep:
`setup → refresh → 12 section analyzers`. Use it to rebuild the full
cache after uploading a new portfolio or at the start of a session.

### Portfolio file upload

The Settings tab has a web upload form that accepts `.csv`, `.tsv`,
`.xls`, `.xlsx`, `.pdf`, `.json`, `.ofx`, and `.qfx` files. The form
sanitizes the filename, writes the file to `/data/portfolios/` inside
the container, and queues a refresh automatically.

### API key configuration

All 8 provider keys are configurable via the Settings tab form (no
shell or container restart required):

| Key | Provider | Purpose |
|---|---|---|
| `TOGETHER_API_KEY` | Together AI | Narrative synthesis (required for prose output) |
| `OPENAI_API_KEY` | OpenAI | Alternative narrative provider |
| `FINNHUB_KEY` | Finnhub | Real-time quotes + analyst ratings |
| `FRED_API_KEY` | FRED | Treasury yields + economic indicators |
| `NEWSAPI_KEY` | NewsAPI | Per-symbol + market-wide news |
| `ALPHA_VANTAGE_KEY` | Alpha Vantage | Quote fallback |
| `MASSIVE_API_KEY` | Massive (via Massive) | High-scale quote coverage (200+ symbols) |
| `MARKETAUX_API_KEY` | MarketAux | Alternative news source |

Keys can also be set via the `portfolio_keys_set` MCP tool from your
agent without opening the dashboard.

## Power-User Endpoints

These REST endpoints don't compete with `portfolio_ask` for routing
but are available for power users:

| Endpoint | Use for |
|---|---|
| `GET /healthz` | Liveness + init state probe |
| `GET /api/portfolio/initialize/status` | Init progress JSON |
| `GET /api/portfolio/initialize/stream` | SSE stream of init state changes |
| `GET /api/portfolio/tools` | Self-describing tool catalog |
| `POST /api/portfolio/keys_set` | Set provider keys without restart |

The `dashboard` at `localhost:18092` is a single-page HTML UI with
tabs for Overview · Holdings · Performance · WhatChanged · Scenarios · Bonds · Optimize · Cashflow · Peer · Analyst · News · Markets · Lookup · Synthesis · Reports · Settings · About.

## Recommended Model Combinations

InvestorClaw uses two LLM roles when answering: **narrative**
(synthesizes the signed envelope into prose) and **validator** (checks
the narrative against the envelope for fabrication and number
preservation).

### Claude Code / Claude Desktop

The agent's own Anthropic LLM does both — no external API key needed.

- **Narrative**: Haiku 4.5 — fast, cheap, ~10× lower output cost than
  Sonnet. With a clean signed envelope, narrative synthesis is mostly
  transcription.
- **Validator**: Sonnet 4.6 (default) or Opus 4.7 (escalation) — gates
  Haiku's output for fabrication, mis-quoted numbers, training-leak
  drift.

Cost-shaped: cheap model on the long output, smart model on the short
safety check. Total session cost on a 100-position portfolio typically
lands well under $0.01.

### openclaw / zeroclaw / hermes

Bring a non-Anthropic provider via `TOGETHER_API_KEY` (or equivalent).
Anthropic on the claws stack is a paid-API-only path since 2026-04-04
(OAuth-subscription tokens against a claws-agent runtime violate
Anthropic's ToS). Fleet defaults:

- **Default narrative**: Together AI `google/gemma-4-31B-it` —
  serverless, ~100 tok/s, ~$0.0008 / 1 K tokens. Container default.
- **Higher-quality alternative**: Together AI `MiniMaxAI/MiniMax-M2` —
  larger context, but moved off Together's serverless tier 2026-05;
  requires a paid dedicated endpoint.
- **Local-only / offline**: Ollama `gemma4:e4b` on host — zero cloud
  cost, GPU-bound, no key required.

## Recommended API Keys by Portfolio Size

| Size | Required | Recommended | Why |
|---|---|---|---|
| **≤ 50 symbols** | `TOGETHER_API_KEY` (narrative) | — | yfinance handles quotes/history at this scale |
| **50–200 symbols** | `TOGETHER_API_KEY` | `FINNHUB_KEY` (free 60/min) + `NEWSAPI_KEY` (free 100/day) | Real-time quotes + analyst + per-symbol news without yfinance throttle |
| **200+ symbols** | `TOGETHER_API_KEY` + `MASSIVE_API_KEY` (Massive, paid) | `FINNHUB_KEY` + `MARKETAUX_API_KEY` (free 100/day) + `FRED_API_KEY` (free, registration) + `ALPHA_VANTAGE_KEY` (free 25/day) | Yahoo's anonymous endpoint rate-limits globally on 200+ symbols; Massive is required, the rest fill analyst + news + yields |

`TOGETHER_API_KEY` is the only key that meaningfully changes output
quality. Everything else is for scale or richness on larger portfolios.
The deterministic engine works key-less in degraded mode (yfinance-only)
but the narrator returns stub catalog summaries instead of real prose.

Sign-up links (free tiers exist for everything except Massive):
[Together AI](https://api.together.ai/settings/api-keys) ·
[Finnhub](https://finnhub.io/register) ·
[Massive](https://massive.com/dashboard/api-keys) ·
[MarketAux](https://www.marketaux.com/account/dashboard) ·
[NewsAPI](https://newsapi.org/register) ·
[FRED](https://fred.stlouisfed.org/docs/api/api_key.html) ·
[Alpha Vantage](https://www.alphavantage.co/support/#api-key)

## How It Works

1. You drop a portfolio (CSV / XLS / PDF / screenshot) into
   `./portfolios/`, or attach one in your agent chat.
2. Your agent calls `portfolio_setup` and `portfolio_ask` over MCP-HTTP
   on `localhost:18090`.
3. ic-engine pre-runs the deterministic backend pipeline for the
   question.
4. The result is stored as an HMAC-signed JSON envelope in
   `./reports/`.
5. A strict narrator receives only the signed envelope and the
   question, quotes verbatim from authoritative sources, and refuses
   to fabricate missing facts.
6. Your agent returns the narrative to you.

The first prompt after a cold install can take 30–60 seconds because
the full deterministic pipeline is building the signed envelope.
Subsequent prompts are cache-amortized (TTL: 30 s for news, 60 s for
other sections) unless you call `portfolio_refresh`.

## Data Privacy

Your data stays on your machine by default.

- Raw broker files stay local in `./portfolios/`
- Account numbers and SSNs are scrubbed on import
- Only computed summaries and the signed envelope are sent to the
  configured narrative provider (Together AI by default)
- InvestorClaw never executes trades, never moves money, never
  authenticates to any brokerage
- All analysis is educational and not investment advice

See [PRIVACY.md](PRIVACY.md) for the full data-handling policy and
[DISCLAIMER.md](DISCLAIMER.md) for the educational-only framing.

## Documentation

- [SKILL.md](SKILL.md) — agent-readable install + usage spec, full
  13-tool catalog, first-run timeline, REST endpoints, troubleshooting
- [PRIVACY.md](PRIVACY.md) — full data-handling policy
- [DISCLAIMER.md](DISCLAIMER.md) — educational-use disclaimer + provider
  data flows
- [SECURITY.md](SECURITY.md) — vulnerability disclosure
- [CONTRIBUTING.md](CONTRIBUTING.md) — contribution workflow
- [CHANGELOG.md](CHANGELOG.md) — release history
- [CAPABILITIES.md](CAPABILITIES.md) — full feature catalog (the
  master "what can it do" doc)
- [STONKMODE.md](STONKMODE.md) — narrated commentary mode + 30
  fictional cable-finance personas
- [docs/GLOSSARY.md](docs/GLOSSARY.md) — financial terminology
  reference (Sharpe, Sortino, YTM, duration, etc.)
- [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md) — "deterministic-first,
  no LLM math" rationale
- [docs/WINDOWS_SETUP_GUIDE.md](docs/WINDOWS_SETUP_GUIDE.md) —
  Windows + WSL2 install gotchas
- [docs/STONKMODE_ARCHITECTURE.md](docs/STONKMODE_ARCHITECTURE.md) —
  Stonkmode pipeline (market detection → archetype weighting → pair
  selection → narration)
- [docs/STONKMODE_AVATAR_LEGEND.md](docs/STONKMODE_AVATAR_LEGEND.md) —
  30-persona avatar reference
- [docs/EOD_REPORT.md](docs/EOD_REPORT.md) — end-of-day report feature walkthrough (what is in the report, how to generate, performance, optional email delivery)
- [docs/MCP_TOOLS_REFERENCE.md](docs/MCP_TOOLS_REFERENCE.md) —
  detailed per-tool reference for all 13 MCP tools (input / output
  schemas, latency, cache TTLs, allowlists, examples)
- [docs/references/](docs/references/) — input / output / schema /
  consultative-LLM contracts (`contract-input.md`, `contract-output.md`,
  `schema-holdings-fields.md`, `runtime-gemma4-consult.md`,
  `presentation-rules.md`, `presentation-nl-query-routing.md`)
- [docs/INSTALL_MODELS.md](docs/INSTALL_MODELS.md) — *why* the v4.x
  architecture splits along two install models
- [docs/COBOL_TESTING.md](docs/COBOL_TESTING.md) — the Agentic COBOL
  250-prompt regression suite that's the v4.x ship gate. Long-form
  rationale at
  [techbroiler.net/all-our-tests-passed-the-agent-was-still-broken](https://techbroiler.net/all-our-tests-passed-the-agent-was-still-broken/).
- [RFC-v0.1.md](RFC-v0.1.md) — full v4.x architecture specification

## Troubleshooting

### "ic-engine container won't start"

```bash
docker compose logs ic-engine | tail -50
docker ps | grep ic-engine
curl -sS http://127.0.0.1:18090/healthz
```

If `healthz` returns `{"init_state":"failed", ...}`, check the
`init_error` field for the engine's exact failure message. The most
common cause is the `portfolios/` directory being root-owned because
you skipped `mkdir -p portfolios` before `docker compose up -d`.

### "No portfolio found"

Drop a CSV/XLS/PDF into `./portfolios/`, then call setup:
```bash
curl -X POST http://127.0.0.1:18090/api/portfolio/setup -d '{}'
```
Or attach a file directly in your agent chat.

### "First call is slow (5–15 minutes)"

Only happens on a cold cache for portfolios with 200+ positions. The
container runs `IC_INITIALIZE_ON_BOOT=1` by default — initialization
runs at container start, so by the time the agent connects, the cache
is warm. Check progress:
`curl http://127.0.0.1:18090/api/portfolio/initialize/status`.

### Reset cache + state

```bash
docker compose down -v   # removes the data volume — all envelopes lost
docker compose up -d     # cold restart with auto-init
```

See [SKILL.md § Troubleshooting](SKILL.md) for the full list.

## Status

Production Ready | Apache 2.0 + MIT-0

InvestorClaw v4.1.x. Portfolio analysis. Educational only. Not
financial advice.

## Related repos

| Repo | Scope |
|---|---|
| [`argonautsystems/InvestorClaw`](https://github.com/argonautsystems/InvestorClaw) (this repo) | v4.x container-first plugin, skill bundle, Docker Compose runtime, and dashboard |
| [`argonautsystems/ic-engine`](https://github.com/argonautsystems/ic-engine) | ic-engine analytical Python source (pulled into the container at build time) |
