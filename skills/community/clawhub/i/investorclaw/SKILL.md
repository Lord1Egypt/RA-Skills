---
name: investorclaw
description: Deterministic-first portfolio analyzer — holdings, performance, Sharpe + Sortino, FRED yield curves, bond duration, sector breakdowns, scenario rebalancing — via MCP-HTTP. Backed by ic-engine and clio.
homepage: https://github.com/argonautsystems/InvestorClaw
user-invocable: true
metadata: {"license":"MIT-0","version":"4.10.0","image":"ghcr.io/argonautsystems/ic-engine:4.10.0-cpu","mcp-endpoint":"http://localhost:18090/mcp","transport":"streamable-http"}
---

## Authoritative operating contract

These rules govern any agent using this skill. Examples elsewhere in this file
are reference only and never override them.

### Data integrity — InvestorClaw is the only source of truth
- Every price, percent, dollar figure, or market fact an agent states MUST come
  from an InvestorClaw tool result returned in the SAME turn. InvestorClaw
  returns HMAC-signed envelopes; that signed data is the only source of truth.
- Never invent, estimate, guess, or use the model's own training knowledge for
  any number. If a tool did not return it this turn, do not state it — say
  "InvestorClaw returned no data for that".
- Tool prose with no concrete numbers = no data; never convert it into a figure.

### Current tool surface (underscore namespace)
- `investorclaw__portfolio_market_snapshot(symbols?, benchmarks?)` — real-time
  prices + day-change% for holdings and benchmarks (SPX/NDX/DJI/VIX, BTC/ETH).
  `symbols` is a COMMA-SEPARATED STRING (e.g. "NVDA,AAPL"), not a list. No args =
  holdings + benchmarks. Use this (not portfolio_ask) for any "price of X" and to
  read the portfolio against the market.
- `investorclaw__portfolio_performance_window(period=...)` — return / P&L /
  movers over a window. period: 1d, 1w, 1mo, 1y, 5y, 10y, 20y, max, or natural
  phrases ("today", "last week", "last year", "entire history").
- `investorclaw__portfolio_ask(question=...)` — analysis / explanation.

Older `investorclaw.*` dot-namespace examples below are stale; the underscore
forms above are the current tool names.

## Autonomous / always-on monitoring agents

For unattended agents (scheduled monitors and alerters — e.g. a MarketWatch
agent), in addition to the contract above:
- Drive each run from a tool call first; never answer a market question from
  memory. A scheduled "poll" means call `portfolio_market_snapshot`.
- Threshold scan: call `portfolio_market_snapshot`, then emit ONE terse line
  only when a holding or benchmark breaches the configured move (e.g. ±3% a
  holding, ±10% VIX); otherwise emit a single `NO_ALERT` token and stop.
- If the required tool errors or returns no data, emit a fixed marker such as
  `OPS_FAIL market_snapshot unavailable` and stop — never fabricate a reassuring
  number to fill the gap.
- No clarifying questions in unattended mode; map intent and act.
- Periodic / EOD reports: pull `portfolio_performance_window` for the window,
  then `portfolio_market_snapshot` for index closes; report numbers verbatim.
- Always read holdings in the context of the benchmarks in the same snapshot.
- Delivery is push, terse, numbers-first. Educational, not personalized advice.


<!--
SPDX-License-Identifier: MIT-0
Copyright 2026 InvestorClaw Contributors
-->

# InvestorClaw — portfolio analysis skill (v4.5.0)

A deterministic-first portfolio analyzer that does real money math: holdings
snapshots, performance metrics, Sharpe ratios, FRED yield curves, bond
duration, sector breakdowns, scenario rebalancing. Backed by ic-engine
(Python, FINOS CDM 5.x compliant).

This skill follows the `compose-x-mcp-services` convention (2026-05-01 RFC; see `RFC-v0.1.md` in this bundle). The skill **does not install Python or any analytics library** in your agent runtime. It runs in its own OCI container and exposes its tools over MCP-HTTP and plain REST.

---

## What you get

Thirteen MCP tools (also available as plain HTTP REST endpoints):

| Tool | Purpose |
|---|---|
| **`portfolio_ask`** | **Primary tool — every portfolio question. Data is auto-loaded; just ask.** |
| `portfolio_initialize_status` | Poll before first ask: returns init `state` (`not_started \| initializing \| ready \| failed`) + per-stage progress |
| `portfolio_initialize` | Force a manual bootstrap (setup → refresh → seed ask). Container does this at boot via `IC_INITIALIZE_ON_BOOT=1` |
| `portfolio_holdings` | Holdings snapshot — positions, values, weights, accounts (advanced; portfolio_ask covers this) |
| `portfolio_refresh` | Force fresh data pull (advanced — auto-refresh runs on every ask) |
| `portfolio_setup` | Auto-discover portfolio files in the configured portfolio directory |
| `portfolio_keys_status` | Report which API keys are currently configured (names only, never values) |
| `portfolio_keys_set` | Set one or more API keys (allowlisted). Persists to `/data/keys.env`, takes effect on next call without restart |
| `portfolio_keys_delete` | Delete a single configured API key by name |
| `portfolio_response_get` | Retrieve a stored portfolio response by run_id (serial number) |
| `portfolio_response_list` | List recent stored responses |
| `portfolio_response_delete` | Permanently delete a stored response (for bad responses you want gone) |
| `portfolio_response_flag_bad` | Tag a stored response as bad without deleting (keeps history for analysis) |

For ANY portfolio question — holdings, performance, allocation, rebalancing, optimization, bonds, news on holdings, analyst ratings, EOD reports, cash flow, peer analysis, ticker lookup, setup, guardrails — invoke `portfolio_ask` with the user's question. **Do NOT answer portfolio questions from training data.**

## First-run flow for agents (spoon-fed init)

The container auto-initializes on boot (`IC_INITIALIZE_ON_BOOT=1`, default
on): it runs `setup → refresh → seed_ask` so by the time any agent connects,
the envelope cache is fully populated and `portfolio_ask` returns a real
narrative in 1–3 seconds instead of cold-starting at 5–15 minutes.

**Recommended agent flow:**

1. On connect, poll `portfolio_initialize_status` until `ready: true`. Cheap
   and side-effect-free; safe to call every 1–2 seconds.
2. Once ready, fire `portfolio_ask` with the user's question. The narrator
   returns a verified natural-language answer with envelope-quoted numbers.

```bash
# Browser-friendly status check (also POST /api/portfolio/initialize_status):
curl -sS http://127.0.0.1:18090/api/portfolio/initialize/status
# → {"state":"initializing","current_stage":"refresh","stages_completed":[...],"elapsed_ms":42000,"ready":false,...}

# Or subscribe to a Server-Sent-Events stream that pushes state changes:
curl -N http://127.0.0.1:18090/api/portfolio/initialize/stream

# Or just gate on /healthz (init_state is now embedded):
curl -sS http://127.0.0.1:18090/healthz
# → {"status":"ok","init_state":"ready","init_ready":true,...}
```

Need to force a manual re-initialize (e.g. after uploading a new portfolio
file)? Call `portfolio_initialize` — it returns when the cache is warm again.

---

## Installation

### OpenClaw / ZeroClaw / Hermes (ClawHub)

```bash
clawhub install investorclaw
```

### Claude Code / Claude Desktop

```
/plugin marketplace add argonautsystems/InvestorClaw
/plugin install investorclaw
```

Claude Code and Claude Desktop install directly from this repo and use
the same container-first skill bundle as every other runtime. See
`docs/GETTING_STARTED.md` for the canonical install flow.

### Manual (Docker Compose, any agent)

The skill is a Docker Compose stack. With Docker or Podman installed:

```bash
mkdir -p portfolios     # IMPORTANT: pre-create so docker doesn't auto-create as root
docker compose up -d    # uses compose.yml shipped in this skill
```

**Agent install convention.** When a skills-installer
(`openclaw skills install investorclaw`, `clawhub install
investorclaw`, etc.) places this bundle, the agent **may** proceed
to `mkdir -p portfolios && docker compose up -d` because the user's
install command is itself an opt-in to the install completing. But
the agent **must** first surface the side effects to the user
explicitly:

1. `docker pull` of `~600 MB` (the engine image) on first run
2. `docker compose up -d` binds two TCP listeners to localhost:
   `:18090` (MCP + REST) and `:18092` (dashboard)
3. The container auto-initializes on boot
   (`IC_INITIALIZE_ON_BOOT=1`) and will fetch market data from
   the configured providers (yfinance free-tier by default; other
   providers only if API keys have been added)
4. Persistent state lands in the `ic-engine-data` Docker volume
   (deleted only by `docker compose down -v`)

A single one-line surfacing covering all four is sufficient. Example:

> Starting the container will pull a ~600 MB image, bind localhost
> ports `:18090` and `:18092`, auto-init against yfinance, and
> persist state in a Docker volume. Proceeding…

The user retains the ability to interrupt (Ctrl-C, "no don't",
etc.). Don't ask a yes/no question by default — that's friction the
user has already cleared by typing the install command. **Do** ask
when one of these conditions holds:

- The host appears to be a CI runner, shared machine, or production
  server where the user might want to review `compose.yml` first.
- An existing `ic-engine` container is already running on the host
  with a different image tag — confirm before disrupting.
- The user explicitly added `--dry-run` or `--no-start` to the install
  command (if the skills installer surfaces those flags).
- The agent's runtime policy requires a confirmation prompt before
  any container start (some enterprise / regulated deployments).

The first command (`mkdir -p portfolios`) is load-bearing. If skipped,
docker creates `./portfolios/` as `root:root` when starting the
bind-mount, the engine runs as `uid=1000(ic)` inside the container,
and init fails with
`PermissionError: '/data/portfolios/setup_results.json'` and the
container goes into `init_state=failed`. Pre-creating the directory
as the host user sidesteps the docker bind-mount UID inheritance
quirk.

The compose pulls `ghcr.io/argonautsystems/ic-engine:4.10.0-cpu` (publicly hosted, no auth) and runs it on `localhost:18090` (MCP + REST) and `localhost:18092` (dashboard).

### If Docker isn't installed

Install Docker Desktop or Docker Engine for your platform — **the user
should run the install themselves** rather than have an agent execute
the command. Pointers (verify with each OS's current docs at
<https://docs.docker.com/engine/install/> before running):

| OS | Suggested path |
|---|---|
| **macOS** | Docker Desktop: <https://docs.docker.com/desktop/install/mac-install/> (Homebrew users: `brew install --cask docker`) |
| **Debian/Ubuntu** | Follow the official guide: <https://docs.docker.com/engine/install/debian/> or <https://docs.docker.com/engine/install/ubuntu/> |
| **Fedora/RHEL** | <https://docs.docker.com/engine/install/fedora/> or <https://docs.docker.com/engine/install/rhel/> |
| **Windows** | Docker Desktop with WSL2 backend: <https://docs.docker.com/desktop/install/windows-install/> |
| **Podman alternative** | `podman compose up -d` is a drop-in replacement once Podman is installed (most distros ship it) |

After install, verify with `docker --version` then run the compose-up
command above.

**For agent operators:** prefer surfacing these install URLs to the
end user rather than running package-manager install commands directly
through your shell tool. Docker installation typically requires sudo
and adds the user to the `docker` group — operations that benefit from
explicit user consent.

### Wait for ready

```bash
until curl -sf http://localhost:18090/healthz > /dev/null 2>&1; do sleep 1; done
echo "ic-engine ready"
```

The first cold-start takes 5-10 seconds (image extract + Python import). Subsequent restarts are <2s.

---

## First-run experience — what to expect

After `docker compose up -d` the container goes through an auto-init
sequence (`IC_INITIALIZE_ON_BOOT=1`) that warms the envelope cache before
your agent talks to it. Expect this timeline on a fresh install:

| Phase | Time | What's happening | What you'll see |
|---|---|---|---|
| Image extract | 5–30 s | First-time pull of `ic-engine:4.10.0-cpu` (~600 MB) | docker compose progress bars |
| Bridge boot | 2–3 s | FastMCP server binds `:18090`, dashboard binds `:18092` | `/healthz` returns 200, `init_state: not_started` |
| `portfolio_setup` | 1–60 s | Auto-discover portfolio files in `./portfolios/` | `init_state: initializing`, `current_stage: setup` |
| `portfolio_refresh` | 30–120 s | Pull quotes / analyst / news / FRED yields for each symbol | `init_state: initializing`, `current_stage: refresh` |
| `seed_ask` | 5–60 s | Run a primer ask so the cache is warm | `init_state: initializing`, `current_stage: seed_ask` |
| **Ready** | — | All sections cached, `portfolio_ask` returns in 1–3 s | `init_state: ready`, `init_ready: true` |

**Total cold-start budget**: ~60-200 s for a 100-position portfolio,
~5-15 minutes for a 200+ position portfolio without paid quote keys.
Watch progress via:

```bash
curl -sS http://127.0.0.1:18090/api/portfolio/initialize/status | jq
# or stream:
curl -N http://127.0.0.1:18090/api/portfolio/initialize/stream
```

### What InvestorClaw asks of you

The container does **not** prompt interactively. It surfaces what it
needs through structured responses:

1. **A portfolio file.** If `./portfolios/` is empty, every `portfolio_ask`
   call returns: *"No portfolio file found … please add CSV/Excel/PDF
   files to your portfolios directory."* Drop a broker export from
   Schwab / Fidelity / Vanguard / UBS / ETrade / Robinhood (CSV/XLS/PDF/screenshot)
   into the bind-mounted `./portfolios/` folder, then call
   `portfolio_setup` to ingest it.

2. **An LLM provider key for narrative synthesis.** Without one, the
   engine still runs the deterministic pipeline (numbers are correct)
   but the narrator returns a stub catalog blurb instead of a real
   prose answer. The container ships pre-configured to use Together AI
   (`google/gemma-4-31B-it`), so all you need is a `TOGETHER_API_KEY`.
   Set it with:

   ```bash
   curl -sS -X POST http://127.0.0.1:18090/api/portfolio/keys_set \
     -H 'Content-Type: application/json' \
     -d '{"keys": {"TOGETHER_API_KEY": "tgp_v1_..."}}'
   ```

   Or drop into the dashboard at http://localhost:18092/ and paste it
   into the Settings tab.

3. **Optional: data-provider keys** for richer / faster results
   on larger portfolios (see *Optional configuration → Which keys to
   obtain (by portfolio size)* below). The engine works key-less in
   degraded mode (yfinance-only, rate-limited).

### What InvestorClaw recommends — by portfolio size

| Size | Required | Recommended | Why |
|---|---|---|---|
| **≤ 50 symbols** | `TOGETHER_API_KEY` (narrative) | — | yfinance handles quotes/history at this scale; one key covers narrative |
| **50–200 symbols** | `TOGETHER_API_KEY` | `FINNHUB_KEY` (free 60/min) + `NEWSAPI_KEY` (free 100/day) | Real-time quotes + analyst + per-symbol news without yfinance throttle |
| **200+ symbols** | `TOGETHER_API_KEY` + `MASSIVE_API_KEY` (Massive, paid) | `FINNHUB_KEY` + `MARKETAUX_API_KEY` (free 100/day) + `FRED_API_KEY` (free, registration) + `ALPHA_VANTAGE_KEY` (free 25/day) | Yahoo's anonymous query1 endpoint rate-limits globally on 200+ symbols under barrage; Massive is required, the rest fill analyst + news + yields |

Why `TOGETHER_API_KEY` is the only hard requirement for narrative:

- Cheapest serverless tier on Together AI (~$0.0008 / 1 K tokens)
- Default model `google/gemma-4-31B-it` has good quality for portfolio
  narrative + ~100 tok/s throughput
- Single key replaces the older multi-tier model setup that v2.x used

Sign-up links (all have free tiers):

| Provider | URL | Free-tier limit |
|---|---|---|
| Together AI | https://api.together.ai/settings/api-keys | $1 free credits |
| Finnhub | https://finnhub.io/register | 60 calls/min |
| Massive (Massive) | https://massive.com/dashboard/api-keys | paid only |
| MarketAux | https://www.marketaux.com/account/dashboard | 100 calls/day |
| NewsAPI | https://newsapi.org/register | 100 calls/day |
| FRED | https://fred.stlouisfed.org/docs/api/api_key.html | unlimited (registration only) |
| Alpha Vantage | https://www.alphavantage.co/support/#api-key | 25 calls/day |

The `TOGETHER_API_KEY` is the only one that's genuinely required.
Everything else degrades gracefully.

### First call — what your agent will see

Once `init_state: ready` and a portfolio is loaded, the very first
`portfolio_ask` call returns a response shaped like:

```json
{
  "exit_code": 0,
  "narrative": "I have holdings summary data in the envelope.\n- bond_pct: 26.76\n- bond_value: 705646.57\n- cash_pct: 1.69\n- equity_pct: 71.55\n- equity_value: 1886470.25\nTop holding symbols: MSFT, NVDA, SCHB, GOOG, AAPL, ...",
  "ic_result": {
    "hmac": "75ca79c...",
    "engine_version": "2.5.2",
    "command": "ask",
    "run_id": "299d36b0-..."
  }
}
```

The `narrative` field is the agent-facing answer. The `ic_result`
contains the HMAC signature that proves the response came from the
deterministic engine (not LLM-fabricated).

If you see *"is a general finance concept. ic-engine is portfolio-specific"*
in the narrative for a question that obviously is about your portfolio,
you're on a pre-v4.1.25 image — pull the latest:

```bash
docker compose pull && docker compose up -d
```

---

## How to call the tools

### Option A: native MCP client (preferred)

If your runtime has a native MCP client, register the server:

```
URL:       http://127.0.0.1:18090/mcp
Transport: streamable-http
Auth:      none (localhost only)
```

Per-runtime CLI:

| Runtime | Command |
|---|---|
| zeroclaw | Add `[[mcp.servers]]` with `name = "ic-engine"`, `url = "http://127.0.0.1:18090/mcp"`, `transport = "http"` to `~/.zeroclaw/config.toml` |
| openclaw | `openclaw mcp set ic-engine '{"url":"http://127.0.0.1:18090/mcp","transport":"streamable-http"}'` |
| hermes | `hermes mcp add ic-engine --url http://127.0.0.1:18090/mcp` |
| claude code | Add to `~/.claude/mcp_servers.json` per Claude Code docs |

Then call tools by name (`portfolio_ask`, `portfolio_holdings`, etc.) via your runtime's tool-use API.

### Option B: plain HTTP REST (works when MCP integration is flaky)

Equivalent endpoints exist at `/api/portfolio/*`. Use your runtime's shell or HTTP tool:

```bash
# Ask any portfolio question
curl -sS -X POST http://127.0.0.1:18090/api/portfolio/ask \
  -H 'Content-Type: application/json' \
  -d '{"question": "What is in my portfolio?"}' \
  --max-time 120

# Other endpoints (no body needed)
curl -sS -X POST http://127.0.0.1:18090/api/portfolio/holdings -H 'Content-Type: application/json' -d '{}'
curl -sS -X POST http://127.0.0.1:18090/api/portfolio/refresh  -H 'Content-Type: application/json' -d '{}'
curl -sS -X POST http://127.0.0.1:18090/api/portfolio/setup    -H 'Content-Type: application/json' -d '{}'

# Self-describing tool catalog
curl -sS http://127.0.0.1:18090/api/portfolio/tools
```

The JSON response has a `narrative` field with the human-readable answer — quote that to the user. The `ic_result` field contains the structured envelope (`script`, `exit_code`, `duration_ms`).

---

## What to ask — example queries

Once installed, ask portfolio questions in natural language. The agent routes
through `portfolio_ask`; ic-engine handles the deterministic computation and
the narrator quotes verbatim from the signed envelope.

| Intent | Example phrasing |
|---|---|
| **Holdings snapshot** | "What's in my portfolio?" • "Show me my positions" • "What do I own?" |
| **Performance** | "How am I doing this year?" • "What's my Sharpe ratio?" • "Show me my drawdowns" |
| **Bonds** | "Show me my bond exposure and yield-to-maturity" • "What's my bond ladder look like?" |
| **Allocation / risk** | "What's my sector exposure?" • "How concentrated is my portfolio?" • "What's my risk profile?" |
| **Optimization / rebalancing** | "Help me rebalance to a 60/40 target" • "Show me an efficient frontier" |
| **Market data** | "What's the current price of NVDA?" • "How is the S&P performing today?" |
| **Fixed-income concepts** | "What does yield-to-maturity mean?" • "Explain duration" |
| **News** | "Today's news on my holdings" • "Crypto news today" |
| **Reports** | "Generate today's EOD report" • "Prepare a full analysis for my advisor meeting" |
| **Fresh data** | "Prices moved — refresh before answering" → triggers `portfolio_refresh` |

The first call after a cold cache may take 30–60 seconds while the
deterministic pipeline builds the signed envelope. Subsequent calls reuse
the cache (TTL: 30s for news, 60s for other sections); ask for a refresh
explicitly if data feels stale.

---

## Agent routing rules

These rules apply when an agent has the InvestorClaw skill installed:

**Use InvestorClaw — do NOT answer from training data, web search, or browsing — for:**
- Any portfolio / holdings / positions question
- Performance, returns, Sharpe/Sortino, drawdown
- Bonds, yield-to-maturity, duration, ladders
- Sector / asset / account allocation
- Optimization, rebalancing, target allocation, scenarios
- Cash flow, dividend / coupon calendars
- Analyst ratings, price targets
- Today's news on holdings or market-wide topics
- Live ticker prices and quotes
- EOD reports, peer comparison, what-changed analysis

**Deterministic-first rules:**
- Never calculate portfolio metrics in the agent — call the tool.
- Never fabricate market, ticker, bond, portfolio, optimization, or news data.
- Preserve quoted source passages, numbers, dates, timestamps, and freshness
  labels exactly.
- If the signed envelope lacks a requested fact, say InvestorClaw did not
  provide it and quote the engine's limitation verbatim.
- Use `portfolio_refresh` only when the user asks for fresh data or when
  data appears stale.

**Attachment handling:**
- When the user attaches a CSV / XLS / XLSX / PDF / screenshot in the same
  turn as a portfolio question, stage the file to the bind-mounted
  `portfolios/` directory, call `portfolio_setup`, then ask the original
  question.
- Do not ask the user to move files manually; the agent owns staging.
- Report low-confidence extraction or setup gaps exactly as InvestorClaw
  returns them.

**Educational guardrails:**
- All output is educational, not investment advice.
- Never present "buy/sell" recommendations as advice.
- Never assess suitability for the user's situation.
- Preserve the engine's disclaimer language verbatim.

---

## Required response format (when answering as an agent)

End every portfolio reply with:

```
Verification: ic-engine ask completed (exit_code: 0)
```

(Substitute the actual `exit_code` from the response.) The harness depends on this exact line.

For finance-concept questions ("what is YTM?") or market-wide questions ("how is the S&P performing?"), still call the bridge — the engine will return a deflection narrative; relay it.

---

## Configure portfolios

Drop your broker exports (CSV, XLS, PDF) into the bind-mounted directory:

```bash
# default mount: ./portfolios on the host -> /data/portfolios in the container
mkdir -p portfolios
cp ~/Downloads/UBS_Holdings_2026-05-02.xls portfolios/

# Then ask the agent or curl the setup endpoint
curl -sS -X POST http://127.0.0.1:18090/api/portfolio/setup -H 'Content-Type: application/json' -d '{}'
```

Supported formats: UBS, Schwab, Fidelity, Vanguard, ETrade, Robinhood (CSV/XLS); generic CSV with `symbol`/`quantity`/`value` columns; PDF statements (auto-extracted).

### Broker export instructions

Most major US brokers expose a CSV download of holdings. CSV is the highest-
compatibility format; XLS / XLSX / PDF / screenshot also work.

| Broker | Path |
|---|---|
| Schwab | Accounts → Positions → Export CSV |
| Fidelity | NetBenefits → Investments → Download CSV |
| Vanguard | My Accounts → Download Holdings |
| UBS | Wealth Management → Holdings → Export |
| ETrade | Portfolio → Holdings → Download |
| Robinhood | Account → Statements → CSV |

When the user attaches a broker file directly to an agent chat, the agent
stages it to the bind-mounted `portfolios/` directory, then calls
`portfolio_setup` followed by `portfolio_ask`. Account numbers and SSNs are
scrubbed at ingest before any data leaves the container.

---

## Optional configuration

The container reads optional env vars from `/data/keys.env` (host-mounted). All optional — the deterministic-engine works without LLM/news keys, just in degraded mode (no narrative synthesis, no live news).

### Which keys to obtain (by portfolio size)

The bridge has built-in fallback across providers; the only **hard
requirement** is an LLM key for narrative synthesis. Below that, your
choice depends on portfolio size.

**Small (≤50 symbols)** — yfinance-only is fine:
- `TOGETHER_API_KEY` (or any LLM): required for narrative
- That's it. Yahoo Finance handles quotes/history at this scale.

**Medium (50–200 symbols)** — add Finnhub:
- `TOGETHER_API_KEY`: LLM narrative
- `FINNHUB_KEY`: real-time quotes + analyst ratings (60/min, free)
- `NEWSAPI_KEY` *(optional)*: per-symbol news (100/day free)

**Large (200+ symbols)** — Massive (Massive) is required:
- `TOGETHER_API_KEY`: LLM narrative
- `MASSIVE_API_KEY` (Massive): paid, un-rate-limited quotes + history
- `FINNHUB_KEY`: analyst ratings + general/forex/crypto/merger news
- `MARKETAUX_API_KEY` *(optional)*: broader news with category filters
- `FRED_API_KEY` *(optional)*: Treasury yield curve (Treasury.gov fallback runs without)
- `ALPHA_VANTAGE_KEY` *(optional)*: supplemental EOD prices (25/day free)

Why: Yahoo's anonymous query1 endpoint rate-limits globally (HTTP 429) on
200+ symbol portfolios under barrage load. Massive (`massive`) handles the
bulk of quotes/history without throttling; Finnhub fills analyst + news;
the no-key Frankfurter (FX) and Treasury Fiscal Data (yields) providers
cover the remainder.

### Full key reference

| Key | Purpose | Cost note |
|---|---|---|
| `TOGETHER_API_KEY` | LLM narrative synthesis (Together google/gemma-4-31B-it) | serverless, fleet default |
| `MASSIVE_API_KEY` | Massive quotes + history (200+ symbol portfolios) | paid, un-rate-limited |
| `MASSIVE_API_KEY` (futures) | CME futures via Massive `/futures/vX` — snapshot + history + correct contract-multiplier notional (ES/NQ/CL/GC/ZB…). Only provider routed for futures. | paid |
| `FINNHUB_KEY` | Real-time quotes + analyst ratings + category news | 60/min free |
| `MARKETAUX_API_KEY` | Financial news with broader filters than NewsAPI | 100/day free |
| `NEWSAPI_KEY` | Per-symbol news (US sources only) | 100/day free |
| `ALPHA_VANTAGE_KEY` | Supplemental EOD prices | 25/day free |
| `FRED_API_KEY` | FRED yield curve | free, registration required |
| `OPENAI_API_KEY` | Alternative LLM (GPT-4o, GPT-5) | paid |

### No-key providers (always available)

| Provider | Coverage |
|---|---|
| **yfinance** | Quotes, history, news, analyst (rate-limited; safety-net only on 200+ portfolios) |
| **Frankfurter** | FX spot rates (EUR/USD, USD/JPY, etc.) — ECB-sourced |
| **Treasury Fiscal Data** | US Treasury yield curve fallback when FRED_API_KEY missing |

### Configure keys via REST/MCP (preferred — no host shell needed)

The agent can set keys directly via the running container, no `/data/keys.env`
edit required. Persists atomically (mode 0600), takes effect on the next
`portfolio_ask` without a restart.

```bash
# What's configured?
curl -sS -X POST http://127.0.0.1:18090/api/portfolio/keys_status \
  -H 'Content-Type: application/json' -d '{}'
# → {"configured":["FINNHUB_KEY","NEWSAPI_KEY"], "settable":[...], "missing":[...]}

# Set one or more keys
curl -sS -X POST http://127.0.0.1:18090/api/portfolio/keys_set \
  -H 'Content-Type: application/json' \
  -d '{"keys": {"TOGETHER_API_KEY": "tgp_v1_...", "FRED_API_KEY": "..."}}'
# → {"configured":["FRED_API_KEY","TOGETHER_API_KEY"], "rejected":[], "deleted":[]}

# Remove a key
curl -sS -X POST http://127.0.0.1:18090/api/portfolio/keys_delete \
  -H 'Content-Type: application/json' -d '{"name": "OPENAI_API_KEY"}'
```

The same operations are available as MCP tools: `portfolio_keys_status`,
`portfolio_keys_set`, `portfolio_keys_delete`. Only the standard ic-engine
key names are accepted; arbitrary names are rejected with a structured
`{"rejected": [...], "settable": [...]}` response.

### Configure keys via host file (alternative)

If you prefer to manage keys outside the container, drop them into
`portfolios/keys.env` on the host (the bind-mounted location), one
`KEY=VALUE` per line:

```env
TOGETHER_API_KEY=tgp_v1_...
FINNHUB_KEY=...
NEWSAPI_KEY=...
```

The container reads from `/data/keys.env` at boot.

---

## Model recommendations

InvestorClaw uses two LLM roles when answering: **narrative** (synthesizes
the signed envelope into prose) and **validator** (checks the narrative
against the envelope for fabrication and number-preservation). The
recommended model mix depends on your runtime.

### Claude Code / Claude Desktop

The agent's own LLM does both roles — no external API key required.

- **Narrative**: Haiku 4.5 — fast, cheap, ~10× lower output cost than
  Sonnet. Synthesis with a clean envelope is mostly transcription, so the
  cheap model is sufficient.
- **Validator**: Sonnet 4.6 (default) or Opus 4.7 (escalation) — gates the
  Haiku output for fabrication, mis-quoted numbers, and training-leak
  drift. Validator output is short (~1 K tokens) so the smart-model bill
  stays low.

This split is cost-shaped: cheap model on the long output, smart model on
the short safety check. Total session cost on a 100-position portfolio
typically lands well under $0.01.

### openclaw / zeroclaw / hermes

**Anthropic on the claws stack — three paths, two of them paid:**
since 2026-04-04 your Anthropic OAuth subscription no longer covers
third-party-tool usage. To use Anthropic models on a claws-agent
runtime you need either (a) Anthropic's discounted "extra usage
bundles" added to your subscription, or (b) a direct Anthropic API
key. Routing OAuth-subscription tokens to a claws-agent without one of
those is a ToS violation per Anthropic's Apr 3 announcement.

Even with paid credits, Anthropic isn't cost-competitive with Together
for InvestorClaw narrative synthesis (~10–50× the per-token cost).
**On our own fleet infrastructure we don't deploy Anthropic for these
runtimes**; end-users should weigh ToS, cost, and quality before
opting into it.

Bring a non-Anthropic provider via `TOGETHER_API_KEY` (or equivalent).
Fleet defaults:

- **Default narrative**: Together AI `google/gemma-4-31B-it` — serverless
  tier, ~100 tok/s, ~$0.0008 / 1 K tokens, ships as the container default.
- **Higher-quality alternative**: Together AI `MiniMaxAI/MiniMax-M2` —
  larger context, but **moved off Together's serverless tier in 2026-05**
  and now requires a paid dedicated endpoint. Use only if you've
  provisioned that endpoint.
- **Local-only / offline**: Ollama `gemma4:e4b` on host — zero cloud cost,
  GPU-bound, no key required.

To switch the narrative model, set `INVESTORCLAW_NARRATIVE_MODEL` in
`portfolios/keys.env` (e.g. `INVESTORCLAW_NARRATIVE_MODEL=MiniMaxAI/MiniMax-M2`
once you have a dedicated endpoint configured at Together).
The container reads it on next call without restart.

---

## Data privacy

**Stays on your machine:**
- Raw broker exports (CSV / XLS / PDF) in `portfolios/`
- Account numbers and SSNs (scrubbed at ingest)
- Full position details (lot history, cost basis)
- Python computation internals (intermediate calculations)

**Sent to the configured LLM provider for narrative synthesis:**
- The user's question
- The HMAC-signed JSON envelope produced by ic-engine
- Computed metrics needed for presentation

**Never sent anywhere:**
- Raw PII (account numbers, SSNs, names)
- Pre-computation intermediate state
- Other portfolios on the same disk

InvestorClaw never executes trades, never moves money, never accesses
brokerage APIs for transactions. Output is educational only.

---

## Verify install + compliance

```bash
# Health check
curl -sS http://127.0.0.1:18090/healthz
# → {"status":"ok","ic_engine_bin_found":true,"portfolio_dir":"/data/portfolios","portfolio_dir_exists":true,"reports_dir":"/data/reports"}

# Smoke test the tool catalog
curl -sS http://127.0.0.1:18090/api/portfolio/tools | python3 -m json.tool

# Smoke test a real question
curl -sS -X POST http://127.0.0.1:18090/api/portfolio/ask \
  -H 'Content-Type: application/json' \
  -d '{"question": "What is in my portfolio?"}' \
  --max-time 120
```

If your agent supports compliance testing, vendor `test_mcp_compliance.py`
from the `mnemos-os/mcp-contracts` GitHub repository into your project, then run:

```bash
python3 test_mcp_compliance.py --url http://127.0.0.1:18090/mcp
```

---

## Dashboard

The container exposes a single-page HTML dashboard on port `:18092`:

```bash
open http://localhost:18092/        # macOS
xdg-open http://localhost:18092/    # Linux
start http://localhost:18092/       # Windows
```

Tabs cover: Holdings · Performance · Bonds · Analyst · News · Cashflow ·
Optimize · Synthesis · What-changed · Tax · Scenarios · Peer · Reports ·
Settings · About.

The dashboard reads the same signed envelope ic-engine produces for
`portfolio_ask`, so metrics stay in sync. Use it for visual review of
holdings / performance, or as a fallback interface when MCP integration
is flaky.

---

## Troubleshooting

### Container won't start

```bash
docker compose logs ic-engine | tail -50
docker ps | grep ic-engine        # confirm running + healthy
curl -sS http://127.0.0.1:18090/healthz
```

If `healthz` returns `{"init_state":"failed", ...}`, check the `init_error`
field for the engine's exact failure message.

### "No portfolio found" when asking

- Drop a CSV / XLS / PDF into `portfolios/` (the host bind mount).
- Then call setup:
  `curl -X POST http://127.0.0.1:18090/api/portfolio/setup -d '{}'`
- Then ask again:
  `curl -X POST http://127.0.0.1:18090/api/portfolio/ask -d '{"question":"what's in my portfolio?"}'`

The agent can stage attached files to `portfolios/` directly when the user
sends them in chat.

### "API key errors" / degraded data

Keys are optional. The deterministic-engine works key-less in degraded
mode (no narrative synthesis, no live news, yfinance-only quotes). To
check what's configured:

```bash
curl -X POST http://127.0.0.1:18090/api/portfolio/keys_status -d '{}'
```

Set the missing key via the REST endpoint shown in
[Optional configuration](#optional-configuration).

### "First call is slow (5–15 minutes)"

Only happens on a cold cache for portfolios with 200+ positions. The
container runs `IC_INITIALIZE_ON_BOOT=1` by default — initialization runs
at container start, so by the time the agent connects, the cache is warm.
If you disabled that env var, expect cold-start latency on first ask.

Check init progress: `curl http://127.0.0.1:18090/api/portfolio/initialize/status`

### "Container is healthy but `portfolio_ask` times out"

- Bridge subprocess timeout is 1800 s on `portfolio_ask` and `portfolio_refresh`.
- Engine P1 parallel-stage timeout is 600 s.
- If you hit either, the engine ran out of upstream API budget (yfinance
  429, Finnhub rate limit, etc.). Switch to Massive (`MASSIVE_API_KEY`)
  for large portfolios; see "Which keys to obtain (by portfolio size)".

### Reset cache + state

```bash
docker compose down -v   # removes the data volume — all envelopes lost
docker compose up -d     # cold restart with auto-init
```

---

## Stop / uninstall

```bash
# Stop (preserves data)
docker compose down

# Stop and remove the data volume
docker compose down -v
```

---

## Security model

InvestorClaw is a single-user, localhost-bound, deterministic-first
analyzer. Several behaviors that automated scanners flag as "warning"
are intentional design choices for this threat model. Documented here
explicitly so reviewers can audit the trade-offs:

| Behavior | Why it's by design |
|---|---|
| **MCP + REST endpoints are unauthenticated on `127.0.0.1:18090`** | Localhost binding (`127.0.0.1:` prefix on the port spec, never `0.0.0.0`) is the security boundary. Any process running as the same user already has filesystem access to portfolios; adding token auth on a loopback API doesn't change that threat model. To expose the service to other hosts, put it behind your own auth layer (Tailscale, nginx + mTLS). |
| **Container auto-initializes on boot** (`IC_INITIALIZE_ON_BOOT=1`) | The cold-cache cost on a 200+ position portfolio is 5–15 minutes; running setup → refresh → seed_ask at boot means agents see `init_state: ready` immediately on connect. Disable with `IC_INITIALIZE_ON_BOOT=0` if you want manual control. The init does not exfiltrate data — it just primes the engine's read-only cache against the providers you've configured. |
| **API keys persist to `/data/keys.env` (mode 0600)** | Keys need to outlive container restarts. The named volume is `ic-engine-data`; on the host that's a docker volume root-owned but only readable by the container's `uid=1000(ic)`. To rotate or delete a key, use `portfolio_keys_set` / `portfolio_keys_delete` — both REST endpoints accept allowlisted names only, never logging values. |
| **Portfolio summaries are sent to the configured narrative LLM provider** | This is the value prop: the engine produces a deterministic envelope, the narrator turns it into prose. To keep narratives local, point `INVESTORCLAW_NARRATIVE_ENDPOINT` at a local Ollama / llama-server / vLLM endpoint (set `INVESTORCLAW_NARRATIVE_PROVIDER=ollama`). To run keyless without any narrator, omit `TOGETHER_API_KEY` — the engine returns a stub catalog summary instead. See [`PRIVACY.md`](PRIVACY.md) for the full data-flow matrix. |
| **Image pulled from `ghcr.io/argonautsystems/ic-engine`** | Pinned to a specific sha256 digest in `compose.yml`, not just the tag — guarantees reproducible builds even if the tag is later mutated. Verify the digest matches what your scanner expects before deploying. Container Apache 2.0 + bridge code MIT-0 in this repo; engine source at `argonautsystems/ic-engine` (pinned by SHA). |

For vulnerability disclosure see [`SECURITY.md`](SECURITY.md). For the
privacy model (what stays local vs what goes to which provider) see
[`PRIVACY.md`](PRIVACY.md).

## Behavior contract

- `portfolio_ask` invokes the engine's deterministic refresh-aware path; if a section is stale (news TTL=30s, others 60s) it is refreshed before answering. Earlier `--no-refresh` short-circuited routing entirely and produced a generic catalog blurb — that flag is intentionally NOT passed.
- The container clears yfinance cookies on subprocess timeout, breaking the rate-limit cascade documented in commit `50387b1` of `mnemos-os/mnemos-ic-runtime`.
- Cross-container reach works via `http://172.17.0.1:18090/mcp` (Docker bridge IP) or via Compose service name `http://ic-engine:8090/mcp` (when both agent + ic-engine are in the same compose).

## Known issues (v4.1.1)

- **Earlier "v4.0.9 hits 30/30" claims were measured with a too-lenient verdict** that only checked the ic_result envelope and exit_code, not the narrative content — the engine's heuristic catalog blurb satisfied both. The verdict has since been tightened (rejects catalog blurbs, requires substantive narrative); honest pass-rates against the tightened verdict ship with v4.1.1 release notes.
- **Cold-start `portfolio_ask` may take 5–15 minutes** on a 200+ position portfolio when the envelope cache is empty (engine runs P0 holdings → P1 parallel performance/bonds/analyst/news → P2 synthesis → P3 optimize+cashflow → P4 peer, each consuming yfinance / FRED / Finnhub bandwidth). Subsequent calls hit the warm cache and return in seconds. Bridge subprocess timeout is 1800s for `portfolio_ask` and `portfolio_refresh`; engine P1 parallel-stage timeout is 600s.

### Fixed in v4.1.1 (was broken in v4.0.x → v4.1.0)

- **Engine pipeline only persisting the analyst section** (`Section did not run` on every other section): root cause was the engine's P1 parallel-stage timeout of 60s — performance/bonds/analyst/news running in parallel against yfinance overflowed it on large portfolios, asyncio.gather raised TimeoutError, the entire P1 result set was lost. Bumped to 600s.
- **Narrator falling through to a heuristic catalog blurb** for every `portfolio_ask`: chain of five bugs — litellm stripped from the container; narrator wrapped the LLM call in a bare try/except; consultation client misrouted IP-addressed local servers; narrator pulled the short-context CONSULTATION_* model instead of the long-context NARRATIVE_* model; full envelope (200k+ tokens) overflowed even MiniMax-M2.7. All five fixed.
- **`--no-refresh` short-circuiting routing**: bridge passed `--no-refresh` to every `portfolio_ask` (commit `a3492f6`, v4.0.7), making the engine return the cached catalog blurb regardless of question. Reverted.

---

## License + provenance

- Service code: Apache 2.0 (`mnemos-os/mnemos-ic-runtime`)
- Distribution-edge artifacts (this `SKILL.md`, `compose.yml`, `install.yaml`, `agent-skills/**`): **MIT-0** (MIT No Attribution — `LICENSE-MIT-0`). Required for ClawHub plugin publishing; the no-attribution clause means downstream skill registries can re-host without preserving copyright notice.
- Image: `ghcr.io/argonautsystems/ic-engine:4.10.0-cpu` (multi-arch amd64+arm64; also at `:latest`)
- RFC: see `RFC-v0.1.md` in this bundle (`mnemos-os/mnemos-ic-runtime` GitHub repository)
- Cross-project contract: `mnemos-os/mcp-contracts` GitHub repository

---

*InvestorClaw is a portfolio analysis service. Educational use only — not investment advice.*
