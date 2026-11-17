<!-- GENERATED FILE — do not edit by hand.
     Regenerate with: python scripts/build_agent_skill.py
     Source of truth: the FastAPI route definitions in backend/routers/. -->

# Oracle-X endpoint reference

Every path below is relative to the instance base URL (`$ORACLE_X_URL`,
default `http://localhost:8000`). Endpoints marked **auth** require
`Authorization: Bearer <supabase-jwt>`; see `auth.md`. Everything else is open
on a default instance.

Request and response bodies are described by their field names and types. When
a response shape is not declared on the route, the entry says so — call it once
and read the actual JSON rather than guessing.

The Turkish market is not here. It is a third of the surface and belongs to a separate skill, `oracle-x-bist`, so that an install that will never ask about Borsa İstanbul does not carry it. If a question names a BIST ticker, a TEFAS fund, KAP or VİOP, say the skill for it exists rather than reaching for `/api/price` — a bare Turkish ticker does not resolve on this surface by design.

## Prices and market state

Spot prices, index levels, candles and derived technical levels.

### `GET /api/price/{symbol}`

Get Symbol Price

Current price for one symbol, crypto or equity.

Exists so the browser does not call an exchange directly: the frontend used
to fetch Binance from the page, which fails outright on the networks where
Binance is blocked and also leaves the browser with no fallback. Routing it
through the backend reuses whichever upstream actually answers.

404 when no price could be resolved — never a placeholder number.

Parameters:
- `symbol` (path, string, required)

Response shape is not declared on the route — inspect one call.

### `GET /api/market-overview`

Get Market Overview

Get market overview with top coin prices and global stats.

Covers the top `TOP_COINS_COUNT` coins by market cap, resolved live from
CoinGecko — no fixed symbol list.


Returns `MarketOverview`: `coins`, `total_volume_24h`, `total_market_cap`, `btc_dominance`, `eth_dominance`, `usdt_dominance`, `active_cryptocurrencies`, `timestamp`, `fear_greed`, `market_status`

### `GET /api/market/indices`

Get Market Indices

Global market indices (S&P 500, NASDAQ, Nikkei, FTSE, DAX, DXY, BIST, …).

Served from the macro board rather than its own fetch. This used to run an
uncached, plainly-headered request per index on every call — which Yahoo
rate-limits — and produced numbers that disagreed with the macro page by
minutes. Sharing the board's cache fixes both, and the response shape is
unchanged so the ticker did not have to move.

An empty list on a total outage, not a 503: this feeds a decorative ticker
strip that is allowed to render nothing.


Response shape is not declared on the route — inspect one call.

### `GET /api/market/candles/{symbol}`

Get Market Candles

Get OHLCV candles for chart backfilling.
Default: 1h interval, 168 candles (1 week).

Parameters:
- `symbol` (path, string, required)
- `interval` (query, string, optional, default `'1h'`)
- `limit` (query, integer, optional, default `168`)

Response shape is not declared on the route — inspect one call.

### `GET /api/technical/{symbol}`

Get Technical Levels

Computed technical levels for a crypto pair or an equity.

Examples: /api/technical/BTCUSDT, /api/technical/BINANCE:ETHUSDT,
/api/technical/AAPL

An unprefixed symbol used to be forced through the crypto path with a
hardcoded "BINANCE:" prefix, which sent tickers like AAPL to the crypto
branch and read them off OKX's tokenised-equity market instead of the
exchange the ticker actually trades on. The prefix is now only added when
the symbol is recognisably a crypto pair.

404 when no levels could be computed — never a placeholder payload.

Parameters:
- `symbol` (path, string, required)

Response shape is not declared on the route — inspect one call.

### `GET /api/asset-detail/{symbol}`

Get Asset Detail

Get detailed asset information.

- **crypto**: CoinGecko data (description, categories, links, ATH/ATL, supply)
- **stock/nasdaq**: Yahoo Finance data (company info, sector, P/E, 52-week range)

Parameters:
- `symbol` (path, string, required)
- `type` (query, string, optional, default `'crypto'`)

Response shape is not declared on the route — inspect one call.

### `GET /api/symbols`

Get Tracked Symbols

Get list of all tracked symbols.


Response shape is not declared on the route — inspect one call.

### `GET /api/heatmap/data`

Get Heatmap Data

Multi-metric heatmap board: price change, volume, turnover, developer.

Answers 503 rather than an empty board when the data cannot be produced —
a blank grid served with a 200 is indistinguishable from a market where
nothing is listed, and the snapshot builder downstream cannot tell them
apart either. A board recovered from the stale cache comes back as a normal
200 carrying `stale: true` and its age.

`include_pegged` brings back stablecoins and wrapped assets, which are
filtered out by default: they read a flat ~0.00% every day and take the
largest tiles on the board while saying nothing about the market.

Parameters:
- `limit` (query, integer, optional, default `50`)
- `include_pegged` (query, boolean, optional, default `False`)

Returns `HeatmapData`: `coins`, `sectors`, `total_market_cap`, `weighted_change_24h`, `weighted_change_7d`, `excluded_pegged`, `unresolved_count`, `timestamp`, `stale`, `age_seconds`

### `GET /api/fear-greed`

Get Fear Greed

Get Crypto Fear & Greed Index from alternative.me API.

Values: 0-25 Extreme Fear, 26-46 Fear, 47-54 Neutral, 55-75 Greed, 76-100 Extreme Greed


Returns `FearGreedData`: `value`, `classification`, `timestamp`, `history`

## News and its analysis

The feed, one article, and the LLM read of an article.

### `GET /api/news`

Get News

Fetch latest news items.

Serves data from memory cache (updated by background scheduler).
If cache is empty (server just started), triggers a fetch.

Parameters:
- `asset_type` (query, string?, optional)
- `limit` (query, integer, optional, default `20`)

Returns `NewsResponse`: `items`, `total`

### `GET /api/news/{news_id}`

Get News Item

Fetch a specific news item by ID.

Parameters:
- `news_id` (path, string, required)

Returns `NewsItem`: `id`, `title`, `summary`, `source`, `published_at`, `symbol`, `asset_type`, `url`

### `GET /api/news/{news_id}/analysis`

Get Cached News Analysis

The stored note for this item, or null if none was produced under the
current pipeline.

Never generates: the caller decides whether to spend the tokens, and this is
what the panel reads when a headline is opened. "Nobody has analysed this
yet" is the ordinary answer on a first click, so it is a null body rather
than a 404 — a 404 here made every first click log a failed request.

Parameters:
- `news_id` (path, string, required)

Returns `NewsAnalysis?`.

### `POST /api/news/{news_id}/analysis/jobs` · **auth**

Start News Analysis

Start the research note for one news item, or re-attach to the running one.

202 for a fresh run, 200 when an identical job is already in flight — a
double click must not fan out into two pipelines.

Parameters:
- `news_id` (path, string, required)
- `current_price` (query, number?, optional)

Response shape is not declared on the route — inspect one call.

### `GET /api/news/analysis/jobs/{job_id}`

Get News Analysis Job

Poll a running analysis. 404 once the job has aged out of retention.

Parameters:
- `job_id` (path, string, required)

Response shape is not declared on the route — inspect one call.

### `POST /api/analyze` · **auth**

Analyze News

Analyze a news item and wait for the result.

Deprecated in favour of the job endpoints above, which report progress
instead of holding the connection open for the whole pipeline. Kept so
existing clients keep working; it returns the legacy `SentimentAnalysis`
subset of the same note.


Body (JSON):
- `news_id` (string, required)
- `current_price` (number?, optional)

Returns `SentimentAnalysis`: `sentiment`, `confidence`, `reasoning`, `historical_context`, `technical_signals`, `prediction_hash`, `tx_hash`, `source`

## Scheduled analysis reports

The long-form daily/weekly reports the terminal generates on a timer.

### `GET /api/analysis/reports`

Get Report Summaries

Freshness metadata for every timeframe.

Read-only and cheap — this is what the Analysis page loads on mount, so it
must never trigger generation.


Response shape is not declared on the route — inspect one call.

### `GET /api/analysis/report/{timeframe}`

Get Analysis Report

Return the stored report for a timeframe, or an empty one if none exists.

Generation is explicitly job-driven; opening the page must not start it.

Parameters:
- `timeframe` (path, string, required)

Response shape is not declared on the route — inspect one call.

### `POST /api/analysis/jobs/{timeframe}` · **auth**

Start Analysis Job

Start generating a report in the background.

If a job for this timeframe is already in flight, its id is returned rather
than starting a second run.

Parameters:
- `timeframe` (path, string, required)

Response shape is not declared on the route — inspect one call.

### `GET /api/analysis/jobs/{job_id}`

Get Analysis Job

Poll a report job for its current stage and, once done, its result.

Parameters:
- `job_id` (path, string, required)

Response shape is not declared on the route — inspect one call.

## Memory and retrieval (RAG)

Historical context: what happened before, what resembles now.

### `GET /api/rag/query`

Query Rag Context

Query RAG 2.0 for historical context.

- q: Query text (e.g., "Bitcoin halving price behavior")
- symbol: Filter by symbol (BTC, ETH, etc.)
- context_type: 'all', 'events', 'prices', 'news'
- asset_type: 'crypto' or 'stock'; keeps the two sides of the catalogue apart

Parameters:
- `q` (query, string, required)
- `symbol` (query, string?, optional)
- `context_type` (query, string, optional, default `'all'`)
- `asset_type` (query, string?, optional)

Response shape is not declared on the route — inspect one call.

### `GET /api/rag/insights/{symbol}`

Get Price Insights

Why is this asset rising/falling?
Correlates price movement with recent news from RAG.

Parameters:
- `symbol` (path, string, required)

Response shape is not declared on the route — inspect one call.

### `GET /api/rag/compare/{symbol_a}/{symbol_b}`

Compare Two Assets

Compare two crypto assets.
Returns price data, events, sentiment, and patterns for both.

Parameters:
- `symbol_a` (path, string, required)
- `symbol_b` (path, string, required)

Response shape is not declared on the route — inspect one call.

### `GET /api/rag/daily-brief`

Get Daily Brief

Generate a comprehensive daily market briefing.
Covers overnight movers, top news, events, and sentiment.


Response shape is not declared on the route — inspect one call.

### `GET /api/rag/anomalies`

Detect Market Anomalies

Detect price-news divergence anomalies.
Flags symbols where price movement doesn't match news sentiment.


Response shape is not declared on the route — inspect one call.

### `GET /api/rag/event-at-date`

Get Event At Date

Find the most significant event near a specific date.
Used for chart tooltip overlays.

Parameters:
- `symbol` (query, string, optional, default `'BTC'`)
- `date` (query, string, optional, default `''`)

Response shape is not declared on the route — inspect one call.

### `POST /api/rag/news-similarity`

Find News Similarity

Find similar historical news and their price outcomes.
Returns how similar past events affected prices.


Body (JSON):
- `title` (string, required)
- `summary` (string, optional)

Response shape is not declared on the route — inspect one call.

### `POST /api/rag/scenario`

Simulate Scenario Endpoint

Simulate a scenario based on historical data.
Example: "What if Bitcoin ETF is rejected?"


Body (JSON):
- `scenario` (string, required)
- `symbol` (string, optional)

Response shape is not declared on the route — inspect one call.

### `GET /api/rag/stats`

Get Rag Statistics

Get RAG 2.0 statistics.


Response shape is not declared on the route — inspect one call.

## Macro

Cross-asset state: indices, metals, the regime label and its evidence.

### `GET /api/macro/board`

Get Macro Board

Commodities, global indices and macro ratios in one cached payload.


Response shape is not declared on the route — inspect one call.

### `GET /api/macro/elections`

Get Elections

Upcoming national elections, priced where a market can be matched to one.

503s with the board rather than with the regime, and for the board's reason:
an empty list here would assert that no election is scheduled anywhere on
Earth. A missing *odds* layer is different and does not 503 — the payload
reports `odds_available: false` and the panel names the outage, because
dates with no prices still say something true.


Response shape is not declared on the route — inspect one call.

### `GET /api/macro/regime`

Get Macro Regime

The cross-asset regime read, plus the note explaining it.

The label and the score are computed in Python and are always present; the
note is decoration and may be absent, still being written, or unavailable
because the model layer is off. The page renders in every one of those cases.

Notes are written on the server's own provider chain rather than a signed-in
user's, because one note is generated per board state and served to everyone
who loads the page. Routing it through a user's own key would bill one reader
for every other reader's copy.


Response shape is not declared on the route — inspect one call.

### `GET /api/macro/pizza-index`

Get Pizza Index

The Pentagon Pizza Index.

Deliberately the one endpoint on this router that cannot fail. The two above
answer 503 because an empty macro board would misstate an outage as a market
with nothing to report; this one carries an OSINT novelty, and the same logic
runs the other way — a scrape that broke must not be able to take the page
its panel sits on down with it. The service answers `status: "unavailable"`
instead, which the panel renders as its own state.


Response shape is not declared on the route — inspect one call.

### `GET /api/macro/neh-index`

Get Neh Index

The Nothing Ever Happens Index.

Cannot fail, for the reason the pizza endpoint cannot: the two share one
panel, and a failure of either has to arrive as a reading that says so
rather than as an error the panel has no shape for.


Response shape is not declared on the route — inspect one call.

## Chains

Per-chain metrics and anomalies measured against each chain's baseline.

### `GET /api/chains/board`

Get Chains Board

Every chain's current state: height, cadence, load, fees and economics, with
the last blocks each one produced.

`fetch_board` does not raise, so the guard here is for the unexpected rather
than for upstream failure — and even then it replays the last good board
before giving up, since a two-minute-old set of heights is far closer to the
truth than nothing.


Response shape is not declared on the route — inspect one call.

### `GET /api/chains/anomalies`

Get Chain Anomalies

What on the board is not normal, and a note explaining why they co-occur.

A second endpoint, on a router whose docstring argues for one — and for the
same reason it argues that. The board is folded together because every
reading on it shares a ten-second cache and comes out of the same requests.
These do not: they are measured against days of history and the note is held
for an hour, so folding them in would ship one hourly artifact on all three
hundred and sixty board polls an hour and pin it to a ten-second cache.

`anomalies` is computed in Python and is the product; the note is commentary
on it. An unreachable model costs the sentence, never the detection.


Response shape is not declared on the route — inspect one call.

## Derivatives and on-chain flow

Liquidations, funding, and large-transaction flow.

### `GET /api/home/liquidations`

Get Liquidations

Get recent liquidations from the OKX liquidation-orders stream.


Response shape is not declared on the route — inspect one call.

### `GET /api/home/funding-rates`

Get Funding Rates

Get real-time funding rates for the core OKX perpetuals, plus any outlier.


Response shape is not declared on the route — inspect one call.

### `GET /api/derivatives/open-interest/{symbol}`

Open Interest

Open interest per exchange, aligned index-for-index with price candles.

`source` says which provider answered: `coinalyze` reaches back years on the
daily series, `venues` is the exchanges' own ~30-day statistics endpoints.
The returned `interval` reports what was actually served, which can be
coarser than the one asked for when a provider does not publish it.

Parameters:
- `symbol` (path, string, required)
- `interval` (query, '1h' | '4h' | '1d', optional, default `'1d'`)
- `limit` (query, integer, optional, default `400`)

Response shape is not declared on the route — inspect one call.

### `GET /api/liquidations/levels/{symbol}`

Get Liquidation Levels

Get observed liquidations grouped into price bins.
A histogram of liquidations that happened, not modelled levels —
for the forward-looking estimate use /api/liquidations/map/{symbol}.

Parameters:
- `symbol` (path, string, required)
- `price_min` (query, number, required)
- `price_max` (query, number, required)
- `num_bins` (query, integer, optional, default `100`)

Response shape is not declared on the route — inspect one call.

### `GET /api/liquidations/map/{symbol}`

Get Liquidation Map Route

Get the modelled liquidation heatmap (Coinglass-style) for a symbol.

These are *estimated* liquidation levels derived from open interest, volume
and the long/short ratio — not observed liquidations. See
`services/liquidation_map_service` for the model and its assumptions.

`venue` picks whose book is modelled, from that venue's own statistics.
There is no `all` here, unlike the profile: this chart's price grid and time
axis both come from one venue's candles.

Parameters:
- `symbol` (path, string, required)
- `interval` (query, string, optional, default `'1h'`)
- `columns` (query, integer, optional, default `160`)
- `bins` (query, integer, optional, default `120`)
- `venue` (query, 'okx' | 'binance' | 'bybit', optional, default `'okx'`)

Response shape is not declared on the route — inspect one call.

### `GET /api/liquidations/lines/{symbol}`

Get Liquidation Lines Route

Get the same modelled liquidation map as spans rather than as a grid.

Each span runs from the column a level was opened at to the column price
swept it, and carries the leverage tier that produced it — the two things
the heatmap's cells collapse. `/api/liquidations/levels/{symbol}` is a
different thing entirely: that one counts liquidations that were observed.

`venue` carries the same meaning and the same caveat as on the map route.

Parameters:
- `symbol` (path, string, required)
- `interval` (query, string, optional, default `'1h'`)
- `columns` (query, integer, optional, default `160`)
- `bins` (query, integer, optional, default `120`)
- `venue` (query, 'okx' | 'binance' | 'bybit', optional, default `'okx'`)

Response shape is not declared on the route — inspect one call.

### `GET /api/liquidations/profile/{symbol}`

Get Liquidation Profile Route

Get the standing modelled liquidation book as a price profile.

The same simulation as the heatmap, stopped at the newest candle and kept
split by leverage tier: one entry per `[bin, tier_index, side, notional]`.
There is no time axis — `price` is the close the two sides divide at.

`venue` picks whose book: one exchange, or `all` for every one of them
re-binned onto a shared grid and summed.

Parameters:
- `symbol` (path, string, required)
- `interval` (query, string, optional, default `'1h'`)
- `columns` (query, integer, optional, default `160`)
- `bins` (query, integer, optional, default `120`)
- `venue` (query, 'okx' | 'binance' | 'bybit' | 'all', optional, default `'okx'`)

Response shape is not declared on the route — inspect one call.

### `GET /api/onchain/whales`

Get Whale Trades

Get whale trade activity from OKX public trades.


Response shape is not declared on the route — inspect one call.

## Ownership

Who holds what, and how those positions moved.

### `GET /api/ownership/board`

Get Ownership Board

Every tracked entity with its allocation and source badge.


Returns `models__ownership__OwnershipBoard`: `entities`, `latest_moves`, `category_counts`, `sources`, `as_of`, `last_refresh_at`, `next_refresh_at`, `stale`

### `GET /api/ownership/consensus`

Get Ownership Consensus

What the tracked holders agree on: most held, most bought, most sold.


Response shape is not declared on the route — inspect one call.

### `GET /api/ownership/assets/{symbol}`

Get Asset Owners

Every tracked holder of one asset.

An empty list is a real answer here — nobody we follow holds it — so this
is a 200 rather than a 404.

Parameters:
- `symbol` (path, string, required)

Response shape is not declared on the route — inspect one call.

### `GET /api/ownership/moves`

Get Ownership Moves

Recent buys, sells and transfers across every tracked holder.

The one endpoint here allowed to answer with an empty list: a quiet period
genuinely has no moves, and saying so is a real answer rather than an
outage dressed up as data.

Parameters:
- `limit` (query, integer, optional, default `30`)
- `category` (query, string?, optional)
- `entity_id` (query, string?, optional)

Returns `models__ownership__Move[]`.

### `GET /api/ownership/flow-note`

Get Flow Note

What the tracked institutions did last quarter, narrated.

The only ownership endpoint that does not 503 when the board is missing. The
others are the page; this is a paragraph above it, and an outage here should
cost the paragraph rather than raise a second error for something the page
has already reported from its own board query.

`facts` carries the deterministic aggregation and renders whether or not the
note itself arrives.


Response shape is not declared on the route — inspect one call.

## Live feeds

Events and the trade tape.

### `GET /api/live/events`

Get Live Events

Scheduled market-moving events, partitioned into live / upcoming / recent.


Response shape is not declared on the route — inspect one call.

### `GET /api/live/tape`

Get Live Tape

Market-moving headlines, newest first.

Reads the news cache the scheduler already refreshes every two minutes, so
polling this costs nothing upstream.

Parameters:
- `limit` (query, integer, optional, default `50`)

Response shape is not declared on the route — inspect one call.

## Chat (authenticated)

The Oracle itself — the terminal's own reasoning layer over all of the above.

### `GET /api/chat/status`

Chat Status

Check if Oracle chat is available, and which provider is serving it.


Response shape is not declared on the route — inspect one call.

### `POST /api/chat` · **auth**

Oracle Chat

Chat with Oracle AI assistant.

Provides intelligent responses about crypto, stocks, and market analysis.
Uses extended thinking time for quality responses.


Body (JSON):
- `message` (string, required)
- `history` (ChatMessage[]?, optional)
- `session_id` (string?, optional)
- `style` (string?, optional)
- `focus_override` (string?, optional)

Returns `ChatResponse`: `response`, `thinking_time`, `sources`, `detected_symbol`, `focus_inherited`, `intent`, `citations`, `followups`, `session_title`

### `POST /api/chat/jobs` · **auth**

Start Chat Job

Start a turn as a background job the client polls.

Same pipeline as `POST /api/chat`; the difference is that the steps are
reported while they run instead of the connection being held open until an
answer exists.


Body (JSON):
- `message` (string, required)
- `history` (ChatMessage[]?, optional)
- `session_id` (string?, optional)
- `style` (string?, optional)
- `focus_override` (string?, optional)

Response shape is not declared on the route — inspect one call.

### `GET /api/chat/jobs/{job_id}` · **auth**

Get Chat Job

Poll a chat job.

404 rather than 403 on someone else's job: a chat job holds a question and
its answer, and confirming that an id exists is already more than a stranger
should learn.

Parameters:
- `job_id` (path, string, required)

Response shape is not declared on the route — inspect one call.

## Prediction markets

What people are betting happens next, and a sourced read on why.

The analysis endpoint may answer with a refusal instead of a verdict. That is a successful run, not an error: the pipeline declines when the evidence it could gather does not support a judgement, and the payload names every search it ran and every one that came back empty. A refusal still carries the market's odds, movement and holder concentration, all of which are measured rather than modelled.

Why a market was opened is a separate job with its own endpoints. It is the one surface here allowed to answer without a source: when no dated reporting explains an opening, it returns `status: conjectured` and a `conjecture` naming the kind of event that usually opens a market like this one. Treat that field as a hypothesis, never as a finding — it carries no source id and is never used to write a verdict.

### `GET /api/polymarket/board`

Get Polymarket Board

Active prediction markets by 24-hour volume.

Carries its own `stale` flag and age so the UI can say how old the odds are
instead of implying they are live.


Response shape is not declared on the route — inspect one call.

### `GET /api/polymarket/markets/{slug}`

Get Polymarket Market

One market's facts and microstructure. No model is consulted.

404 when the slug resolves to nothing — never a placeholder market.

Parameters:
- `slug` (path, string, required)

Response shape is not declared on the route — inspect one call.

### `GET /api/polymarket/map`

Get Polymarket Map

Three geographic layers, each labelled with what it actually is.

None of them is "where the money came from" — that cannot be built from
Polymarket's data and the payload says so per layer rather than leaving the
reader to assume. See `services/polymarket/map_service`.


Response shape is not declared on the route — inspect one call.

### `POST /api/polymarket/markets/{slug}/analysis/jobs` · **auth**

Start Polymarket Analysis

Start the bet analysis for one market, or re-attach to the running one.

202 for a fresh run, 200 when an identical job is already in flight — a
double-clicked Analysis button must not pay for two pipelines.

The job may well end in a refusal rather than a verdict, and that is a
successful run: the pipeline declines when the evidence it could gather does
not support a judgement, and says which searches came back empty.

Parameters:
- `slug` (path, string, required)

Response shape is not declared on the route — inspect one call.

### `GET /api/polymarket/analysis/jobs/{job_id}`

Get Polymarket Analysis Job

Poll a running analysis. 404 once the job has aged out of retention.

Parameters:
- `job_id` (path, string, required)

Response shape is not declared on the route — inspect one call.

### `POST /api/polymarket/markets/{slug}/origin/jobs` · **auth**

Start Polymarket Origin

Start the "why was this bet opened" trace, or re-attach to the running one.

A separate job from the verdict on purpose. The two are started by the same
click and answer different questions at different speeds, and holding the
origin answer back until the sweep and two synthesis calls have finished
would hide a result that was ready in thirty seconds. Neither waits for the
other and neither reads the other's output.

Like the analysis, this may decline: with no dated reporting inside any
window it answers with a labelled hypothesis, and with nothing at all it
answers `undetermined`. Both are successful runs.

Parameters:
- `slug` (path, string, required)

Response shape is not declared on the route — inspect one call.

### `GET /api/polymarket/origin/jobs/{job_id}`

Get Polymarket Origin Job

Poll a running origin trace. 404 once the job has aged out of retention.

Parameters:
- `job_id` (path, string, required)

Response shape is not declared on the route — inspect one call.

## Watchlist (authenticated)

The caller's own tracked symbols.

### `GET /api/home/watchlist` · **auth**

Get Watchlists Endpoint


Response shape is not declared on the route — inspect one call.

### `POST /api/home/watchlist` · **auth**

Create Watchlist Endpoint


Body (JSON):
- `name` (string, required)
- `items` (WatchlistItem[], required)

Response shape is not declared on the route — inspect one call.

## Health

Whether the instance and its upstreams are actually up.

### `GET /api/system/health`

System Health

Per-category health of every upstream the app reads, for the LIVE badge.

Passive: it reports what the last real call to each provider did, and makes
no request of its own. That means it is cheap enough for the frontend's
ten-second poll, and it costs no upstream rate limit.

Public, so `detail` carries only a short failure class — never a URL, a host
or an upstream's own error body.


Response shape is not declared on the route — inspect one call.

### `GET /api/system/readiness`

System Readiness

Startup progress, polled by the frontend's boot gate.

`ready` turns true once every required step has succeeded and every optional
one has settled, or once the warm-up deadline passes — whichever comes
first. `degraded` says the screen opened without everything working, and
`blocked` says a required step failed and waiting will not help.

Cheap by design: it reads in-memory state and performs no I/O, because the
frontend polls it twice a second while the splash is up.


Response shape is not declared on the route — inspect one call.
