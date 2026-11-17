# prediction-markets-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**65 endpoints across 4 platform group(s).**

## Polymarket (30)

### `polymarket_activity_trades`

- **HTTP:** `GET /polymarket/activity/trades`
- **What:** List Polymarket activity trades. Returns public trade rows used by Polymarket's `/activity` page. The `taker_only` enum accepts `true` and `false`; the `filter_type` enum accepts `CASH`; the `filter_amount` enum accepts `1`, `5`, `10`, `100`, `1000`, `10000`, and `100000`.
- **Params:** `event_id` (string, optional) — Optional Polymarket event id; `filter_amount` (string, optional) — Minimum filtered amount; `filter_type` (string, optional) — Activity amount filter type; `limit` (integer, optional) — Maximum trades, defaults to 50 and supports up to 100; `market` (string, optional) — Optional market condition id; `offset` (integer, optional) — Result offset, defaults to 0 and supports up to 10000; `taker_only` (string, optional) — Taker-only filter

### `polymarket_clob_market`

- **HTTP:** `GET /polymarket/clob/market/{condition_id}`
- **What:** Get Polymarket CLOB market. Returns one public CLOB market detail row by market condition id, including tokens, reward settings, order acceptance state, tags, and fees.
- **Params:** `condition_id` (string, **required**) — Polymarket market condition id

### `polymarket_dashboard_macro`

- **HTTP:** `GET /polymarket/dashboards/macro`
- **What:** List Polymarket macro dashboard events. Lists events from Polymarket's macro dashboard, tagged `macro`, up to `limit` events (default 20, max 100). Each event has its title, slug, dates, volume, liquidity, open interest, tags and nested markets with outcomes and prices. Pass the returned `cursor` back to fetch the next page; `has_more` shows whether there is one.
- **Params:** `cursor` (string, optional) — Optional keyset cursor from a prior macro dashboard response; `limit` (integer, optional) — Maximum macro events, defaults to 20 and supports up to 100

### `polymarket_event_detail`

- **HTTP:** `GET /polymarket/event/{slug}`
- **What:** Get Polymarket event detail. Returns one Polymarket event. This endpoint does not require a Polymarket user token, wallet signature, cookies, or personal account authentication.
- **Params:** `slug` (string, **required**) — Polymarket event slug

### `polymarket_event_tags`

- **HTTP:** `GET /polymarket/events/{id}/tags`
- **What:** List tags for a Polymarket event. Lists the tags attached to one Polymarket event, identified by the required event `id`. Each tag has its id, label and slug. An invalid id returns an invalid-parameter error.
- **Params:** `id` (string, **required**) — Polymarket event id

### `polymarket_events`

- **HTTP:** `GET /polymarket/events`
- **What:** List Polymarket events. Lists Polymarket events with their markets. Sort by 24-hour volume, total volume, liquidity, end date and more, filter to open or closed events, and page with `limit` (default 25, max 100) and `offset`. Each event has its slug, description, end date, liquidity, open interest and comment count; each market has its question, outcomes, best bid and ask, last trade price and volume.
- **Params:** `ascending` (boolean, optional) — Sort ascending when true; `closed` (string, optional) — Closed filter; `limit` (integer, optional) — Maximum events, defaults to 25 and supports up to 100; `offset` (integer, optional) — Result offset, defaults to 0 and supports up to 10000; `order` (string, optional) — Sort field

### `polymarket_events_similar`

- **HTTP:** `GET /polymarket/events/similar`
- **What:** Find similar Polymarket events. Finds Polymarket events similar to a given one. Supply at least one of `id`, `event_title`, `event_slug`, `market_title` or `market_slug`; `limit` defaults to 10 (max 50) and `closed` (`true` or `false`) filters by closed state. Each event has its title, dates, volume, liquidity, tags and nested markets.
- **Params:** `closed` (string, optional) — Closed filter; `event_slug` (string, optional) — Event slug; `event_title` (string, optional) — Event title; `id` (integer, optional) — Polymarket event id; `limit` (integer, optional) — Maximum events, defaults to 10 and supports up to 50; `market_slug` (string, optional) — Market slug; `market_title` (string, optional) — Market title

### `polymarket_homepage_feed`

- **HTTP:** `GET /polymarket/homepage/feed`
- **What:** List Polymarket homepage feed rows. Returns rows for Polymarket homepage feeds. The `feed` enum accepts `trending`, `breaking`, `new`, `politics`, `sports`, `crypto`, `esports`, `iran`, `finance`, `geopolitics`, `tech`, `culture`, `economy`, `weather`, `mentions`, and `elections`. Most feeds return events; `breaking` returns high-movement market rows and `mentions` returns open event search matches.
- **Params:** `cursor` (string, optional) — Optional keyset cursor from a prior event feed response; `feed` (string, optional) — Homepage feed; `limit` (integer, optional) — Maximum rows, defaults to 20 and supports up to 100

### `polymarket_leaderboard`

- **HTTP:** `GET /polymarket/leaderboard`
- **What:** List Polymarket leaderboard rows. Returns trader leaderboard rows. The `window` enum accepts `1d`, `7d`, `30d`, and `all`; the `sort_by` enum accepts `profit` and `volume`.
- **Params:** `limit` (integer, optional) — Maximum rows, defaults to 20 and supports up to 100; `sort_by` (string, optional) — Leaderboard sort; `window` (string, optional) — Leaderboard time window

### `polymarket_market_detail`

- **HTTP:** `GET /polymarket/market/{id}`
- **What:** Get Polymarket market detail by id. Returns one Polymarket market. This endpoint does not require a Polymarket user token, wallet signature, cookies, or personal account authentication.
- **Params:** `id` (string, **required**) — Polymarket market id

### `polymarket_market_liquidity`

- **HTTP:** `GET /polymarket/market/{id}/liquidity`
- **What:** Get Polymarket market liquidity. Returns a public market liquidity snapshot that joins market detail with public CLOB market data when token ids are available. This endpoint is not a trading endpoint and does not require a Polymarket user token, wallet signature, cookies, or personal account authentication.
- **Params:** `id` (string, **required**) — Polymarket market id

### `polymarket_market_tags`

- **HTTP:** `GET /polymarket/market/{id}/tags`
- **What:** List tags for a Polymarket market. Lists the tags attached to one Polymarket market, identified by the required market `id`. Each tag has its id, label and slug. An invalid id returns an invalid-parameter error.
- **Params:** `id` (string, **required**) — Polymarket market id

### `polymarket_markets`

- **HTTP:** `GET /polymarket/markets`
- **What:** List Polymarket markets. Lists Polymarket markets, up to `limit` rows (default 25, max 100), starting at `offset` (default 0, max 10000). Sort with `order`, such as `volume24hr` or `liquidity`, flip direction with `ascending`, and filter with `closed`. Each market has its question, slug, prices, volume, liquidity, token ids and outcomes.
- **Params:** `ascending` (boolean, optional) — Sort ascending when true; `closed` (string, optional) — Closed filter; `limit` (integer, optional) — Maximum markets, defaults to 25 and supports up to 100; `offset` (integer, optional) — Result offset, defaults to 0 and supports up to 10000; `order` (string, optional) — Sort field

### `polymarket_predictions`

- **HTTP:** `GET /polymarket/predictions`
- **What:** List Polymarket predictions. Returns event rows for the Polymarket `/predictions` page. The `status` enum accepts `active`, `resolved`, and `all`; the `sort` enum accepts `competitive`, `volume`, `volume_24hr`, `ending_soon`, `liquidity`, `newest`, and `closed_time`; the `recurrence` enum accepts `hourly`, `daily`, `weekly`, `monthly`, and `yearly`.
- **Params:** `cursor` (string, optional) — Optional keyset cursor from a prior predictions response; `limit` (integer, optional) — Maximum events, defaults to 20 and supports up to 100; `recurrence` (string, optional) — Optional recurrence filter; `sort` (string, optional) — Prediction sort; `status` (string, optional) — Prediction status; `tag` (string, optional) — Optional tag slug

### `polymarket_public_data`

- **HTTP:** `GET /polymarket/fee-types`
- **What:** Polymarket fee types. Returns Polymarket's fee type reference data as rows under `data`, optionally narrowed with `active` (`true` or `false`) or a `search` term. The response includes a `fetched_at` time. An invalid `active` value returns an invalid-parameter error.
- **Params:** `active` (string, optional) — Optional upstream active filter; `search` (string, optional) — Optional upstream search filter

### `polymarket_related_tags`

- **HTTP:** `GET /polymarket/tag/{id}/related-tags`
- **What:** Get related Polymarket tags by id. Lists the Polymarket tags related to one tag, identified by the required tag `id`. Optional `omit_empty` (`true` or `false`), `status` and `locale` narrow the result. Each tag has its id, label and slug. An invalid id returns an invalid-parameter error.
- **Params:** `id` (string, **required**) — Polymarket tag id; `locale` (string, optional) — Optional upstream locale; `omit_empty` (string, optional) — Omit empty related tags; `status` (string, optional) — Optional upstream status filter

### `polymarket_rewards_market`

- **HTTP:** `GET /polymarket/rewards/market/{condition_id}`
- **What:** Get Polymarket rewards market. Returns the liquidity-rewards details of one Polymarket market by condition id: the question, daily reward rate, rewards minimum size and maximum spread, each reward configuration with its start and end dates and rate per day, total configured rewards, 24-hour volume and outcome token prices. A condition id with no rewards row returns `404`.
- **Params:** `condition_id` (string, **required**) — Polymarket market condition id

### `polymarket_rewards_markets`

- **HTTP:** `GET /polymarket/rewards/markets`
- **What:** List Polymarket rewards markets. Returns public rewards-market rows used by Polymarket's `/rewards` page. The `order_by` enum accepts `market`, `earnings`, `max_spread`, `min_size`, `rate_per_day`, `price`, `earning_percentage`, and `spread`; the `position` enum accepts `asc` and `desc`; the `tag_slug` enum accepts `all`, `politics`, `sports`, `crypto`, `pop-culture`, `middle-east`, `business`, and `science`.
- **Params:** `cursor` (string, optional) — Optional rewards cursor from a prior response; defaults to MA==; `date` (string, optional) — Reward program date in YYYY-MM-DD format; defaults to today in UTC; `limit` (integer, optional) — Maximum rows, defaults to 100 and supports up to 100; `order_by` (string, optional) — Rewards market sort; `position` (string, optional) — Sort direction; `q` (string, optional) — Optional market question search text; `tag_slug` (string, optional) — Rewards category

### `polymarket_search`

- **HTTP:** `GET /polymarket/search`
- **What:** Search Polymarket events. Searches Polymarket and returns event results. The `status` enum accepts `open`, `closed`, and `all`; the `sort` enum accepts `relevance`, `volume24hr`, `volume`, `liquidity`, and `endDate`.
- **Params:** `ascending` (boolean, optional) — Sort ascending when true; `include_profiles` (boolean, optional) — Include matching profiles; `include_tags` (boolean, optional) — Include matching tags; `limit` (integer, optional) — Maximum events, defaults to 10 and supports up to 50; `q` (string, **required**) — Search query; `sort` (string, optional) — Search sort; `status` (string, optional) — Event status filter

### `polymarket_tag`

- **HTTP:** `GET /polymarket/tag/{id}`
- **What:** Get a Polymarket tag by id. Returns one Polymarket tag by its required `id`: its id, label and slug. Optional `include_template` and `locale` adjust the lookup. An invalid id returns an invalid-parameter error.
- **Params:** `id` (string, **required**) — Polymarket tag id; `include_template` (boolean, optional) — Include upstream template data when supported; `locale` (string, optional) — Optional upstream locale

### `polymarket_tags`

- **HTTP:** `GET /polymarket/tags`
- **What:** List Polymarket tags. Lists Polymarket tags, up to `limit` rows (default 25, max 100), starting at `offset` (default 0, max 10000). Sort with `order` and flip direction with `ascending` (`true` or `false`); `locale` is optional. Each tag has its id, label and slug.
- **Params:** `ascending` (string, optional) — Sort ascending flag; `limit` (integer, optional) — Maximum tags, defaults to 25 and supports up to 100; `locale` (string, optional) — Optional upstream locale; `offset` (integer, optional) — Result offset, defaults to 0 and supports up to 10000; `order` (string, optional) — Sort field

### `polymarket_token_midpoint`

- **HTTP:** `GET /polymarket/token/{token_id}/midpoint`
- **What:** Get Polymarket token midpoint. Returns the current midpoint price for one Polymarket outcome token, identified by the required `token_id`, as a single `midpoint` number such as 0.285. It is a read-only snapshot, returned with a `fetched_at` time and the `token_id`, and is not investment advice.
- **Params:** `token_id` (string, **required**) — Polymarket CLOB token id

### `polymarket_token_orderbook`

- **HTTP:** `GET /polymarket/token/{token_id}/orderbook`
- **What:** Get Polymarket token order book. Returns the order book for one Polymarket outcome token, identified by the required `token_id`. The `book` has `bids` and `asks` as price and size pairs, the last trade price, tick size, minimum order size, condition id and a timestamp. Prices and sizes are numbers.
- **Params:** `token_id` (string, **required**) — Polymarket CLOB token id

### `polymarket_token_price`

- **HTTP:** `GET /polymarket/token/{token_id}/price`
- **What:** Get Polymarket token price. Returns the current price for one Polymarket outcome token, identified by the required `token_id`. `side` is `buy` or `sell` and defaults to `buy`. The response gives the `price` as a number, the `side` used and a `fetched_at` time. It is a snapshot, not trading advice.
- **Params:** `side` (string, optional) — Order side used for the CLOB price; `token_id` (string, **required**) — Polymarket CLOB token id

### `polymarket_token_price_history`

- **HTTP:** `GET /polymarket/token/{token_id}/price-history`
- **What:** Get Polymarket token price history. Returns price history points for one Polymarket outcome token, identified by the required `token_id`. `interval` is one of `1m`, `1h`, `6h`, `1d` (default), `1w`, `all` or `max`; `fidelity` sets minutes per point (0 means 60, max 1440); `start_ts` and `end_ts` bound the range. Each point has a Unix `timestamp` and `price`. No points returns 404.
- **Params:** `end_ts` (integer, optional) — Optional Unix timestamp upper bound; `fidelity` (integer, optional) — Data point resolution in minutes; 0 uses the default 60; maximum 1440; `interval` (string, optional) — History interval; `start_ts` (integer, optional) — Optional Unix timestamp lower bound; `token_id` (string, **required**) — Polymarket CLOB token id

### `polymarket_token_spread`

- **HTTP:** `GET /polymarket/token/{token_id}/spread`
- **What:** Get Polymarket token spread. Returns the current bid-ask spread for one Polymarket outcome token, identified by the required `token_id`, as a single `spread` number. It is a read-only snapshot with a `fetched_at` time and is not investment advice.
- **Params:** `token_id` (string, **required**) — Polymarket CLOB token id

### `polymarket_tokens_midpoints`

- **HTTP:** `POST /polymarket/tokens/midpoints`
- **What:** Get Polymarket token midpoints. Returns public CLOB midpoints for up to 25 Polymarket token ids. This does not require a Polymarket user token, wallet signature, cookies, or personal account authentication.
- **Params:** `body` (object, **required**) — Token ids request body
- **REST body:** Send the value of the MCP argument `body` directly as the JSON body; do not wrap it in a `body` property.

### `polymarket_tokens_orderbooks`

- **HTTP:** `POST /polymarket/tokens/orderbooks`
- **What:** Get Polymarket token order books. Returns public CLOB order-book depth for up to 25 Polymarket token ids. This does not require a Polymarket user token, wallet signature, cookies, or personal account authentication.
- **Params:** `body` (object, **required**) — Token ids request body
- **REST body:** Send the value of the MCP argument `body` directly as the JSON body; do not wrap it in a `body` property.

### `polymarket_tokens_prices`

- **HTTP:** `POST /polymarket/tokens/prices`
- **What:** Get Polymarket token prices. Returns public CLOB buy and sell prices for up to 25 Polymarket token ids. The `side` enum accepts `buy` and `sell`; when omitted, both sides are returned. This does not require a Polymarket user token, wallet signature, cookies, or personal account authentication.
- **Params:** `body` (object, **required**) — Token ids request body
- **REST body:** Send the value of the MCP argument `body` directly as the JSON body; do not wrap it in a `body` property.

### `polymarket_tokens_spreads`

- **HTTP:** `POST /polymarket/tokens/spreads`
- **What:** Get Polymarket token spreads. Returns public CLOB spreads for up to 25 Polymarket token ids. This does not require a Polymarket user token, wallet signature, cookies, or personal account authentication.
- **Params:** `body` (object, **required**) — Token ids request body
- **REST body:** Send the value of the MCP argument `body` directly as the JSON body; do not wrap it in a `body` property.

## Kalshi (21)

### `kalshi_event`

- **HTTP:** `GET /kalshi/event/{event_ticker}`
- **What:** Kalshi event detail. Returns one Kalshi event by `event_ticker` (such as `KXELONMARS-99`) together with its markets. The event has its series ticker, title, subtitle, category, strike period and mutually-exclusive flag; each market has prices, bid and ask, volume, open interest, status and rules. An unknown ticker returns a not-found error.
- **Params:** `event_ticker` (string, **required**) — Kalshi event ticker

### `kalshi_event_history`

- **HTTP:** `GET /kalshi/event/{event_ticker}/history`
- **What:** Kalshi event history. Returns candlesticks for the markets in a Kalshi event, grouped by market, for `event_ticker`. `start_ts` defaults to 7 days ago, `end_ts` to now, `period_interval` to 1440 minutes, and `series_ticker` to the ticker prefix before the last dash. Each candle has price, yes bid and ask, volume and open interest. Ranges are capped at 366 days.
- **Params:** `end_ts` (integer, optional) — Unix end timestamp in seconds. Defaults to now.; `event_ticker` (string, **required**) — Kalshi event ticker; `include_latest_before_start` (boolean, optional) — Include the latest candle before start_ts when supported upstream.; `period_interval` (integer, optional) — Candlestick interval in minutes. Default: 1440.; `series_ticker` (string, optional) — Kalshi series ticker. Defaults to the event ticker prefix before the last dash.; `start_ts` (integer, optional) — Unix start timestamp in seconds. Defaults to 7 days ago.

### `kalshi_event_metadata`

- **HTTP:** `GET /kalshi/event/{event_ticker}/metadata`
- **What:** Kalshi event metadata. Returns the media and market metadata for one Kalshi event by `event_ticker`. The response has the event image and featured image, a color code and image for each market, settlement sources with name and URL, and competition context when it applies. An unknown ticker returns a not-found error.
- **Params:** `event_ticker` (string, **required**) — Kalshi event ticker

### `kalshi_events`

- **HTTP:** `GET /kalshi/events`
- **What:** Kalshi events. Lists Kalshi events, up to `limit` rows (default 25, max 200), continued with `cursor`. Filter by `series_ticker`, `category`, `status` (`open`, `closed` or `settled`), `min_close_ts` and `min_updated_ts`. `with_nested_markets` adds each event's markets. Each event has its ticker, title, category and strike period. A `cursor` is returned when more rows exist.
- **Params:** `category` (string, optional) — Kalshi category filter; `cursor` (string, optional) — Pagination cursor from a previous Kalshi response; `limit` (integer, optional) — Rows to return, default 25, max 200; `min_close_ts` (integer, optional) — Minimum event close Unix timestamp in seconds; `min_updated_ts` (integer, optional) — Minimum event update Unix timestamp in seconds; `series_ticker` (string, optional) — Kalshi series ticker filter; `status` (string, optional) — Event status filter; `with_milestones` (boolean, optional) — Include event milestones when supported upstream; `with_nested_markets` (boolean, optional) — Include nested market rows when supported upstream

### `kalshi_exchange_schedule`

- **HTTP:** `GET /kalshi/exchange/schedule`
- **What:** Kalshi exchange schedule. Returns the Kalshi exchange schedule, with no inputs. `standard_hours` are date-bounded blocks listing `open_time` and `close_time` for each weekday, and `maintenance_windows` list start time, end time and reason. The maintenance list can be empty. Informational only.
- **Params:** _none_

### `kalshi_exchange_status`

- **HTTP:** `GET /kalshi/exchange/status`
- **What:** Kalshi exchange status. Returns the current Kalshi exchange status, with no inputs: `exchange_active` says whether the exchange is up, and `trading_active` says whether trading is open at the time of the request. Informational only, not real-time trading data.
- **Params:** _none_

### `kalshi_historical_cutoff`

- **HTTP:** `GET /kalshi/historical/cutoff`
- **What:** Kalshi historical data cutoff. Returns the three cutoff timestamps Kalshi uses to split live from historical data: `market_settled_at`, `orders_updated_at` and `trades_created_at`. Use them to decide when settled market data should be read from the historical endpoints. Takes no parameters.
- **Params:** _none_

### `kalshi_historical_market`

- **HTTP:** `GET /kalshi/historical/market/{ticker}`
- **What:** Kalshi historical market detail. Returns one settled Kalshi market from historical storage by `ticker`. The response has the title, subtitle, event ticker, status, result, open, close and expiration times, last and previous price, yes and no bid and ask, volume, open interest, liquidity and primary rules text. Invalid tickers are rejected.
- **Params:** `ticker` (string, **required**) — Kalshi historical market ticker

### `kalshi_historical_market_history`

- **HTTP:** `GET /kalshi/historical/market/{ticker}/history`
- **What:** Kalshi historical market history. Returns candlesticks for one settled Kalshi market by `ticker`. `start_ts` defaults to 7 days ago, `end_ts` to now and `period_interval` to 1440 minutes. Each candle has end time, price, yes bid and ask, volume and open interest. Ranges are capped at 366 days.
- **Params:** `end_ts` (integer, optional) — Unix end timestamp in seconds. Defaults to now.; `period_interval` (integer, optional) — Candlestick interval in minutes. Default: 1440.; `start_ts` (integer, optional) — Unix start timestamp in seconds. Defaults to 7 days ago.; `ticker` (string, **required**) — Kalshi historical market ticker

### `kalshi_historical_markets`

- **HTTP:** `GET /kalshi/historical/markets`
- **What:** Kalshi historical markets. Returns settled Kalshi historical market rows. `tickers`, `event_ticker`, and `series_ticker` are mutually exclusive. The `mve_filter` enum accepts `exclude`.
- **Params:** `cursor` (string, optional) — Pagination cursor from a previous Kalshi response; `event_ticker` (string, optional) — Kalshi event ticker filter. Mutually exclusive with tickers and series_ticker.; `limit` (integer, optional) — Rows to return, default 25, max 1000; `mve_filter` (string, optional) — Multivariate event filter; `series_ticker` (string, optional) — Kalshi series ticker filter. Mutually exclusive with tickers and event_ticker.; `tickers` (string, optional) — Comma-separated Kalshi market tickers. Mutually exclusive with event_ticker and series_ticker.

### `kalshi_historical_trades`

- **HTTP:** `GET /kalshi/historical/trades`
- **What:** Kalshi historical trades. Lists older Kalshi trades that have moved into historical storage, up to `limit` rows (default 25, max 200), continued with `cursor`. Filter by market `ticker` and by created time with `min_ts` and `max_ts` (Unix seconds). Each trade has its id, count, yes and no price, taker side and created time.
- **Params:** `cursor` (string, optional) — Pagination cursor from a previous Kalshi response; `limit` (integer, optional) — Rows to return, default 25, max 200; `max_ts` (integer, optional) — Maximum created Unix timestamp in seconds; `min_ts` (integer, optional) — Minimum created Unix timestamp in seconds; `ticker` (string, optional) — Kalshi market ticker filter

### `kalshi_market`

- **HTTP:** `GET /kalshi/market/{ticker}`
- **What:** Kalshi market detail. Returns one Kalshi market by `ticker` (such as `KXELONMARS-99`). The response has the title, subtitle, event ticker, status, result, open, close and expiration times, last and previous price, yes and no bid and ask, volume, 24-hour volume, open interest, liquidity and rules text. An unknown ticker returns a not-found error.
- **Params:** `ticker` (string, **required**) — Kalshi market ticker

### `kalshi_market_history`

- **HTTP:** `GET /kalshi/market/{ticker}/history`
- **What:** Kalshi market history. Returns candlesticks for one Kalshi market by `ticker`. `series_ticker` defaults to the ticker prefix before the last dash, `start_ts` to 7 days ago, `end_ts` to now and `period_interval` to 1440 minutes. `include_latest_before_start` adds the last candle before the start. Ranges are capped at 366 days.
- **Params:** `end_ts` (integer, optional) — Unix end timestamp in seconds. Defaults to now.; `include_latest_before_start` (boolean, optional) — Include the latest candle before start_ts when supported upstream.; `period_interval` (integer, optional) — Candlestick interval in minutes. Default: 1440.; `series_ticker` (string, optional) — Kalshi series ticker. Defaults to the market ticker prefix before the last dash.; `start_ts` (integer, optional) — Unix start timestamp in seconds. Defaults to 7 days ago.; `ticker` (string, **required**) — Kalshi market ticker

### `kalshi_market_orderbook`

- **HTTP:** `GET /kalshi/market/{ticker}/orderbook`
- **What:** Kalshi market orderbook. Returns the order book for one Kalshi market by `ticker`: bid levels for the `yes` side and the `no` side, each with `price` and `size`. Kalshi publishes bids only, so ask levels are not listed. The response also carries a `raw_unit_hint` for the price unit.
- **Params:** `ticker` (string, **required**) — Kalshi market ticker

### `kalshi_markets`

- **HTTP:** `GET /kalshi/markets`
- **What:** Kalshi markets. Lists Kalshi markets, up to `limit` rows (default 25, max 200), continued with `cursor`. Filter by `event_ticker`, `series_ticker`, `ticker`, or `status` (`unopened`, `open`, `closed` or `settled`). Each market has its title, status, prices, bid and ask, volume, open interest and rules text. A returned status can read `active` even though the filter does not accept it.
- **Params:** `cursor` (string, optional) — Pagination cursor from a previous Kalshi response; `event_ticker` (string, optional) — Kalshi event ticker filter; `limit` (integer, optional) — Rows to return, default 25, max 200; `series_ticker` (string, optional) — Kalshi series ticker filter; `status` (string, optional) — Market status filter; `ticker` (string, optional) — Kalshi market ticker filter

### `kalshi_markets_history`

- **HTTP:** `GET /kalshi/markets/history`
- **What:** Kalshi batch market history. Returns candlesticks for up to 25 Kalshi markets in one call. `market_tickers` is required, as a comma-separated list or repeated values. `start_ts` defaults to 7 days ago, `end_ts` to now and `period_interval` to 1440 minutes. Results are grouped by market. Ranges are capped at 366 days.
- **Params:** `end_ts` (integer, optional) — Unix end timestamp in seconds. Defaults to now.; `include_latest_before_start` (boolean, optional) — Include the latest candle before start_ts when supported upstream.; `market_tickers` (string, **required**) — Comma-separated Kalshi market tickers. Repeated query values are also accepted.; `period_interval` (integer, optional) — Candlestick interval in minutes. Default: 1440.; `start_ts` (integer, optional) — Unix start timestamp in seconds. Defaults to 7 days ago.

### `kalshi_markets_orderbooks`

- **HTTP:** `GET /kalshi/markets/orderbooks`
- **What:** Kalshi batch market orderbooks. Returns order books for up to 25 Kalshi markets in one call. `tickers` is required, as a comma-separated list or repeated values. Each book has the `yes` and `no` bid levels with `price` and `size`; ask levels are not listed. Books come back in the order requested.
- **Params:** `tickers` (string, **required**) — Comma-separated Kalshi market tickers. Repeated query values are also accepted.

### `kalshi_multivariate_events`

- **HTTP:** `GET /kalshi/events/multivariate`
- **What:** Kalshi multivariate events. Lists Kalshi multivariate events, which the regular events list leaves out, up to `limit` rows (default 25, max 200), continued with `cursor`. Each event has its ticker, series ticker, title, subtitle, category and markets. A `cursor` is returned when more rows exist.
- **Params:** `cursor` (string, optional) — Pagination cursor from a previous Kalshi response; `limit` (integer, optional) — Rows to return, default 25, max 200

### `kalshi_series`

- **HTTP:** `GET /kalshi/series`
- **What:** Kalshi series. Lists Kalshi series, up to `limit` rows (default 25, max 200). Each series has its ticker, title, category, frequency, fee type and multiplier, settlement sources, and contract and contract-terms URLs. The catalogue comes back in one page, so `cursor` has no effect on this endpoint.
- **Params:** `cursor` (string, optional) — Pagination cursor from a previous Kalshi response; `limit` (integer, optional) — Rows to return, default 25, max 200

### `kalshi_series_detail`

- **HTTP:** `GET /kalshi/series/{series_ticker}`
- **What:** Kalshi series detail. Returns one Kalshi series by `series_ticker` (such as `KXELONMARS`). The response has the title, category, frequency, fee type and multiplier, settlement sources with name and URL, contract and contract-terms URLs, and last update time. An unknown ticker returns a not-found error.
- **Params:** `series_ticker` (string, **required**) — Kalshi series ticker

### `kalshi_trades`

- **HTTP:** `GET /kalshi/trades`
- **What:** Kalshi trades. Lists recent Kalshi trades, up to `limit` rows (default 25, max 200), continued with `cursor`. Filter by market `ticker` and by created time with `min_ts` and `max_ts` (Unix seconds, at most 366 days apart). Each trade has its id, count, yes and no price, taker side and created time.
- **Params:** `cursor` (string, optional) — Pagination cursor from a previous Kalshi response; `limit` (integer, optional) — Rows to return, default 25, max 200; `max_ts` (integer, optional) — Maximum created Unix timestamp in seconds; `min_ts` (integer, optional) — Minimum created Unix timestamp in seconds; `ticker` (string, optional) — Kalshi market ticker filter

## Metaculus (11)

### `metaculus_category_questions`

- **HTTP:** `GET /metaculus/category/{slug}/questions`
- **What:** Metaculus category questions. Returns Metaculus question rows for a category. Allowed category slugs: artificial-intelligence, computing-and-math, cryptocurrencies, economy-business, elections, environment-climate, geopolitics, health-pandemics, law, metaculus, natural-sciences, nuclear, politics, social-sciences, space, sports-entertainment, technology.
- **Params:** `limit` (integer, optional) — Rows to return, default 10, max 25; `slug` (string, **required**) — Metaculus category slug

### `metaculus_comments_feed`

- **HTTP:** `GET /metaculus/comments-feed`
- **What:** Metaculus comments feed. Returns Metaculus question rows for the questions referenced by the most recent public comments, in comment recency order. Comment bodies are not exposed.
- **Params:** `limit` (integer, optional) — Rows to return, default 10, max 25; `topic` (string, optional) — Optional Metaculus topic slug

### `metaculus_project_questions`

- **HTTP:** `GET /metaculus/project/{slug}/questions`
- **What:** Metaculus project questions. Returns Metaculus question rows for one public project, filtered by its slug. A slug that does not exist returns 404.
- **Params:** `limit` (integer, optional) — Rows to return, default 10, max 25; `slug` (string, **required**) — Metaculus project slug

### `metaculus_question`

- **HTTP:** `GET /metaculus/question/{id}`
- **What:** Metaculus question detail. Returns one Metaculus question by numeric `id` (a question or post id). The response has the title, status, question type, unit, open, close and resolve times, forecaster and forecast counts, comment count, latest forecast center and bounds, categories, projects and URL.
- **Params:** `id` (string, **required**) — Metaculus question or post id

### `metaculus_question_forecast_history`

- **HTTP:** `GET /metaculus/question/{id}/forecast-history`
- **What:** Metaculus question forecast history. Returns public aggregation forecast history points for one Metaculus question. The `method` enum accepts `recency_weighted`, `unweighted`, and `single_aggregation`.
- **Params:** `id` (string, **required**) — Metaculus question or post id; `max_points` (integer, optional) — Maximum history points to return, default 500, max 2000; `method` (string, optional) — Aggregation method

### `metaculus_question_forecasts`

- **HTTP:** `GET /metaculus/question/{id}/forecasts`
- **What:** Metaculus question forecasts. Returns the latest forecast summary per aggregation method for one Metaculus question, by numeric `id`. Each method has its name, forecaster count, center, lower and upper values, and number of history points. `recency_weighted`, `unweighted` and `single_aggregation` are listed first when present. The question details come with it.
- **Params:** `id` (string, **required**) — Metaculus question or post id

### `metaculus_question_metadata`

- **HTTP:** `GET /metaculus/question/{id}/metadata`
- **What:** Metaculus question metadata. Returns public metadata for one Metaculus question, including option labels, option history, scaling metadata, resolution fields, and timing fields when present.
- **Params:** `id` (string, **required**) — Metaculus question or post id

### `metaculus_question_options`

- **HTTP:** `GET /metaculus/question/{id}/options`
- **What:** Metaculus question options. Returns public multiple-choice option labels and latest option-level forecast values for one Metaculus question. The `method` enum accepts `recency_weighted`, `unweighted`, and `single_aggregation`.
- **Params:** `id` (string, **required**) — Metaculus question or post id; `method` (string, optional) — Aggregation method

### `metaculus_questions`

- **HTTP:** `GET /metaculus/questions`
- **What:** Metaculus questions. Returns Metaculus question rows. The endpoint fails closed, returning an error instead of partial data, when the source responds with an authenticated-only response or a challenge page.
- **Params:** `limit` (integer, optional) — Rows to return, default 10, max 25; `topic` (string, optional) — Optional Metaculus topic slug

### `metaculus_top_comments`

- **HTTP:** `GET /metaculus/top-comments`
- **What:** Metaculus top comments feed. Returns Metaculus question rows for the questions whose recent public comments collected the highest vote scores over roughly the last week. Comment bodies are not exposed.
- **Params:** `limit` (integer, optional) — Rows to return, default 10, max 25; `topic` (string, optional) — Optional Metaculus topic slug

### `metaculus_tournament_questions`

- **HTTP:** `GET /metaculus/tournament/{slug}/questions`
- **What:** Metaculus tournament questions. Returns Metaculus question rows for one public tournament, filtered by its slug. A slug that does not exist returns 404.
- **Params:** `limit` (integer, optional) — Rows to return, default 10, max 25; `slug` (string, **required**) — Metaculus tournament slug

## DraftKings Predictions (3)

### `draftkings_predictions_availability`

- **HTTP:** `GET /draftkings/predictions/availability`
- **What:** DraftKings Predictions availability map. Returns the 52 region/status mappings shown on DraftKings Predictions' public availability map. Allowed `status` values: `all_markets_available`, `financial_markets_only`, `sports_markets_unavailable`, `no_markets_available`. This source map is not a complete legal eligibility matrix and does not separately classify all territories or tribal land. It does not read caller location or trading/account state.
- **Params:** _none_

### `draftkings_predictions_categories`

- **HTTP:** `GET /draftkings/predictions/categories`
- **What:** DraftKings Predictions categories. Returns the public category and league navigation from the DraftKings Predictions homepage. It excludes market quotes, trade-slip selections, accounts, balances, promotions, and location data. Market availability varies by location and time; this endpoint is a navigation directory, not trading advice.
- **Params:** _none_

### `draftkings_predictions_rules`

- **HTTP:** `GET /draftkings/predictions/rules`
- **What:** DraftKings Predictions rules and settlement sources. Lists public rulebook and settlement-source links from the DraftKings Predictions Rules and Settlements page. It does not fetch market data, quotes, trades, user state, or location context.
- **Params:** _none_
