---
name: oracle-x-api
description: Read live market intelligence from a running Oracle-X terminal — spot prices and candles for crypto (BTC, ETH, SOL) and equities, computed support/resistance zones, news with its LLM analysis, macro regime, per-chain metrics, liquidations, funding rates, open interest, whale flow, institutional ownership, Polymarket prediction-market odds, and a vector memory of past market events. Use this whenever the user asks what an asset is doing, why it moved, where its levels are, what the news means, how the macro backdrop looks, who is holding it, what the market odds on an event are, or what happened last time conditions looked like this — and whenever ORACLE_X_URL is set or something is listening on localhost:8000. Prefer it over generic web search for anything the terminal already tracks, because the terminal's numbers are cached, cross-checked and timestamped. Borsa İstanbul is deliberately not here — BIST, TEFAS, KAP and VİOP are the sibling skill oracle-x-bist, on the same instance.
version: "1.3.0"
license: Complete terms in LICENSE.txt
metadata:
  homepage: "https://github.com/Yigtwxx/OracleX"
  openclaw:
    emoji: "🔮"
    homepage: "https://github.com/Yigtwxx/OracleX"
    requires:
      anyBins:
        - curl
        - python3
    primaryEnv: ORACLE_X_URL
    envVars:
      - name: ORACLE_X_URL
        required: false
        description: Base URL of the running Oracle-X instance. Defaults to http://localhost:8000.
      - name: ORACLE_X_TOKEN
        required: false
        description: Supabase access token, needed only for the chat and watchlist endpoints.
---

# Oracle-X

Oracle-X is a self-hosted financial intelligence terminal: a FastAPI backend
that pulls equities and digital assets into one universe, keeps a vector memory
of what it has seen, and reasons over both through an LLM layer the operator
chooses. This skill is the read side of that backend.

**Prerequisite: an instance has to be running.** This skill talks to a server;
it is not a data source of its own. If nothing answers, say so — do not fall
back to remembered prices. A number invented for a trading question is worse
than no number.

## Setup

Two environment variables, and neither belongs in a file you write:

| Variable | Meaning |
|---|---|
| `ORACLE_X_URL` | Instance base URL. Default `http://localhost:8000`. |
| `ORACLE_X_TOKEN` | Supabase JWT, only for the authenticated endpoints. |

Confirm the instance is alive before the first real call:

```bash
curl -sf "${ORACLE_X_URL:-http://localhost:8000}/api/system/health" | head -c 400
```

`/api/system/health` is passive — it reports what the last real call to each
upstream did and issues no requests of its own, so polling it costs nothing.
A category reporting `degraded` there explains an empty payload downstream
better than any retry will.

If the connection is refused, tell the user the terminal is not running and
stop. If a specific category is down, answer with what the healthy categories
returned and name the gap.

## Choosing an endpoint

Most requests are one call. Find the row, read the endpoint's full parameters
in `references/endpoints.md`, call it.

| The user wants | Call | Why this one |
|---|---|---|
| A current price | `GET /api/price/{symbol}` | Resolves crypto and equities through whichever upstream answers; 404 means unresolved, never a placeholder. |
| The state of the market | `GET /api/market-overview` | Top coins, dominance, global volume and sentiment in one payload. |
| Index levels (S&P, NASDAQ, DXY, …) | `GET /api/market/indices` | Shares the macro board's cache, so it agrees with the macro page. |
| Support, resistance, RSI, trend | `GET /api/technical/{symbol}` | Zones are built per timeframe and scored by how many horizons confirm them. Do not recompute this from candles. |
| Raw OHLCV | `GET /api/market/candles/{symbol}` | Only when you genuinely need the series — for levels, use `/api/technical`. |
| Company fundamentals | `GET /api/asset-detail/{symbol}?type=stock` | P/E, sector, 52-week range, analyst targets. `type=stock` is required for equities; the crypto branch resolves through CoinGecko and 404s on a symbol it cannot map. |
| Sentiment | `GET /api/fear-greed` | Both the crypto and equity gauges. |
| Latest news | `GET /api/news?limit=…&asset_type=…` | Served from the scheduler's cache. |
| What a specific article means | `GET /api/news/{news_id}/analysis` | The cached LLM read. If absent, start a job (below). |
| A market-wide written report | `GET /api/analysis/report/{timeframe}` | The stored daily/weekly report. Reading never triggers generation. |
| Macro backdrop | `GET /api/macro/board` | Indices, metals, commodities, ratios. |
| "What kind of market is this?" | `GET /api/macro/regime` | A computed label and score, plus a written note. The label is always present; the note may not be. |
| The odds on an event happening | `GET /api/polymarket/board` | Live prediction markets by volume. A price here is what traders believe, not evidence about the world. |
| Why a market moved, or why it exists | `POST /api/polymarket/markets/{slug}/analysis/jobs` | Traces sharp price moves to dated news and weighs both sides. May refuse; a refusal names what it searched. |
| Chain activity, fees, congestion | `GET /api/chains/board` | Per-chain metrics under one adapter contract. |
| Something unusual on-chain | `GET /api/chains/anomalies` | Measured against each chain's own baseline, not a global threshold. |
| Liquidations | `GET /api/home/liquidations`, `GET /api/liquidations/map/{symbol}` | Aggregate first, then the per-symbol map. `/levels/` is a histogram of what already happened and needs `price_min` and `price_max`; `/map/` is the forward-looking estimate and needs neither. |
| Funding / leverage positioning | `GET /api/home/funding-rates` | |
| Whale movement | `GET /api/onchain/whales` | Large-transaction flow with direction. |
| Who holds this stock | `GET /api/ownership/assets/{symbol}` | Institutional positions for one ticker. |
| What holders are doing overall | `GET /api/ownership/consensus`, `GET /api/ownership/moves` | Consensus is the state; moves are the deltas. |
| "Has this happened before?" | `GET /api/rag/query?q=…&symbol=…` | The vector memory. This is the reason to prefer Oracle-X over a search engine. |
| History behind one symbol | `GET /api/rag/insights/{symbol}` | |
| Two assets compared | `GET /api/rag/compare/{a}/{b}` | |
| A briefing to start the day | `GET /api/rag/daily-brief` | |
| "What if X happened?" | `POST /api/rag/scenario` | Grounded in stored history rather than free speculation. |
| An open-ended question | `POST /api/chat` (auth) | The terminal's own reasoning layer, with tools over everything above. |
| The user's tracked symbols | `GET /api/home/watchlist` (auth) | |

Anything not in this table is in `references/endpoints.md` — read that before
inventing a path. Guessed URLs return 404s that look like missing data.

**Borsa İstanbul is not on this surface.** A bare Turkish ticker does not
resolve through `/api/price`, by design. BIST equities, TEFAS funds, KAP
disclosures and VİOP live behind `/api/bist/*` and belong to the sibling skill
`oracle-x-bist` — same instance, same base URL, installed separately so that an
agent that will never be asked about Turkey does not carry a third of the
allowlist. If a question names one, say the skill for it exists rather than
guessing a path.

## Rules that keep the answer honest

These matter more than endpoint coverage, because the failure they prevent is
the one that costs the user money.

**Report what the API returned, and nothing else.** A 404 from `/api/price` or
`/api/technical` means the symbol could not be resolved — the backend
deliberately refuses to emit a placeholder. Say "the terminal has no price for
that symbol" rather than supplying one from memory.

**Do not recompute what the terminal computed.** `/api/technical` already
builds zones per timeframe and scores them by confluence. Deriving your own
support level from candles produces a number that contradicts what the user
sees on their own screen, which is worse than not answering.

**Reach for `/api/chat` deliberately.** It runs the full planner and costs an
LLM call on the operator's own provider budget. For "what is BTC trading at",
call `/api/price`. For "should I be worried about this setup", the chat
endpoint is the right tool — it has the same data plus the memory and the
reasoning. Check `GET /api/chat/status` first; it says whether a provider is
actually serving.

**Timestamps are part of the answer.** Most payloads carry one. Market data
without a time is a claim about now that may be about an hour ago; quote it.

**Send the symbol in the form the endpoint expects.** Crypto pairs are
`BTCUSDT` or `BINANCE:ETHUSDT`; equities are the plain ticker with
`?type=stock` where the route takes one. A 404 on a symbol you believe exists
is usually the wrong form rather than missing data — `references/endpoints.md`
records which routes care.

**Fan out rather than asking one endpoint to do everything.** There is no
single "tell me about X" call. A full read on an asset is four independent
requests — price, technicals, leverage, memory — and since none depends on
another they cost one round trip when issued together.
`references/recipes.md` has the sequence.

## Long-running work: the job pattern

Analysis and chat generation take minutes, so they are not held open on a
connection. Three endpoints follow the same shape — start, then poll:

| Start | Poll | Note |
|---|---|---|
| `POST /api/analysis/jobs/{timeframe}` (auth) | `GET /api/analysis/jobs/{job_id}` | An in-flight job returns its existing id rather than starting a second run. |
| `POST /api/news/{news_id}/analysis/jobs` | `GET /api/news/analysis/jobs/{job_id}` | Check `GET /api/news/{news_id}/analysis` first — it may already be cached. |
| `POST /api/chat/jobs` (auth) | `GET /api/chat/jobs/{job_id}` | Same pipeline as `POST /api/chat`, but the steps are reported while they run. |

Poll on an interval of a few seconds and give up after a couple of minutes with
an explanation, rather than blocking indefinitely. `examples/03_chat_job.py`
implements this loop.

## Authentication

Most of what an agent needs is open on a default instance: prices, technicals,
news, macro, chains, liquidations, ownership, RAG. Authentication is needed
only for endpoints scoped to a person — chat, watchlist, and starting an
analysis job.

Send the JWT as `Authorization: Bearer $ORACLE_X_TOKEN`. Read it from the
environment; never write it into a file, a URL, or a log line. If it is absent
and the user's question needs an authenticated endpoint, ask them for it rather
than falling back to an unauthenticated call that will 401.

A 404 on `GET /api/chat/jobs/{job_id}` may mean the job belongs to someone
else — the backend answers 404 rather than 403 there on purpose, so do not read
it as "the job vanished".

`references/auth.md` covers where a token comes from and how to test one.

## A first call

```bash
BASE="${ORACLE_X_URL:-http://localhost:8000}"

curl -sf "$BASE/api/price/BTCUSDT"
curl -sf "$BASE/api/technical/AAPL"
curl -sf "$BASE/api/rag/query?q=bitcoin%20halving%20price%20behavior&symbol=BTC"
curl -sf -H "Authorization: Bearer $ORACLE_X_TOKEN" \
     -H 'Content-Type: application/json' \
     -d '{"message":"How does the current BTC setup compare to March?"}' \
     "$BASE/api/chat"
```

Symbols follow the venue: crypto pairs are `BTCUSDT` or `BINANCE:ETHUSDT`,
equities are the plain ticker, `AAPL`. Passing `AAPL` where a pair is expected
used to route an equity through the crypto path; the backend now decides by
inspecting the symbol, but sending the right form is still cheaper.

## When something goes wrong

| Symptom | Reading |
|---|---|
| Connection refused | No instance. Say so and stop; do not answer from memory. |
| 404 on a price or technical call | The symbol could not be resolved. Check the form (`BTCUSDT` vs `BTC`). |
| Empty list, 200 status | The scheduler has not filled that cache yet. Check `/api/system/health` for the category. |
| 401 | Missing or expired `ORACLE_X_TOKEN`. |
| 503 on chat | No LLM provider is currently serving. `GET /api/chat/status` names it. |
| A `stale` flag in the payload | Real data, but the upstream last answered a while ago. Quote it as such. |

## Reference files

Read these on demand rather than upfront:

- **`references/endpoints.md`** — every allowlisted endpoint with its
  parameters, request body and response fields. Generated from the running
  schema, so it matches the deployed API. Consult it before any call that is
  not a plain path from the table above.
- **`references/auth.md`** — obtaining and using a token, and which endpoints
  need one.
- **`references/recipes.md`** — the multi-step reads: a full asset workup, a
  news-to-thesis pass, a macro-plus-chains regime check.
- **`examples/`** — runnable Python (`httpx`) for the client, the job polling
  loop, and a complete asset workup.
