---
name: ibkr-httpapi
description: HTTP+JSON control plane over Interactive Brokers (ib_async + a local IB Gateway container) that the user already runs. Talk to a real brokerage with curl + JSON: market data (OHLC bars, snapshot/historical ticks, option chains + Greeks) across stocks/options/futures/cfd/forex/crypto, account/positions summaries, order placement / retrieval / cancellation, and server-side technical analysis via the wickworks sidecar. Bearer-token auth (API_TOKEN). Use when the user has deployed ibkr-httpapi and set IBKR_HTTPAPI_URL and wants to pull IBKR market data, inspect account/positions, run TA, or place/cancel orders. THIS API CAN PLACE, EXERCISE, AND CANCEL REAL ORDERS ON A REAL IBKR ACCOUNT. Every account-mutating call requires explicit per-action user confirmation.
homepage: https://github.com/psyb0t/ibkr-httpapi
user-invocable: true
metadata:
  { "openclaw": { "emoji": "📈", "primaryEnv": "IBKR_HTTPAPI_URL", "requires": { "bins": ["docker", "curl"] } } }
---

# ibkr-httpapi

HTTP client for an IBKR bridge the user has already deployed. It wraps
Interactive Brokers via [ib_async](https://github.com/ib-api-reloaded/ib_async)
and a Linux-native IB Gateway container, and exposes a curl-friendly JSON
surface: contract details, snapshot + historical ticks, OHLC bars, option
chains with Greeks, account/positions summaries, cross-asset order entry, and
server-side TA via the [wickworks](https://github.com/psyb0t/docker-wickworks)
sidecar. Same operational shape as its sister project
[mt5-httpapi](https://github.com/psyb0t/mt5-httpapi): one bridge, one token,
same asset-class routing model.

This skill talks to a **running** ibkr-httpapi server. It does not stand one
up, does not provision IBKR credentials, and does not place trades on its own
initiative.

## Security & safety

**Destructive & irreversible.** `POST /orders` places a REAL order on a real
IBKR brokerage account. It moves real money and creates live market
activity with no undo. `DELETE /orders/{orderId}` and `DELETE /orders`
cancel real orders; `POST /options/exercise` exercises/lapses real option
contracts. An agent must NEVER call any of these unless the user explicitly
requested that exact action with the specific parameters (symbol, side,
quantity, price). Never infer, extrapolate, or "helpfully" place a related
order. Echo back the resolved symbol/side (`action`)/quantity/price (and
order type) and get explicit user confirmation for that specific order
before sending it. Never auto-retry a rejected or failed order. A rejection
is a stop, not a retry trigger; surface the rejection reason and wait for a
new, explicit instruction. On `DELETE /orders` (global cancel), never
enumerate-then-bulk-cancel without showing the full list and getting the
user's explicit go-ahead for the whole batch first.

**No auth when `API_TOKEN` (`config.yaml:api_token`) is unset.** With it
empty the HTTP API is UNAUTHENTICATED: anyone who can reach the socket
gets full read + order-placement/cancellation access to the account. NEVER
expose such an instance on a network or to untrusted agents; set the token
and keep the deployment bound to loopback / behind an authenticating proxy.

**External transmission.** Every request goes to whatever `IBKR_HTTPAPI_URL`
points at. Market data, account state, and order instructions leave your
host for that endpoint. Point it only at an ibkr-httpapi instance you run or
explicitly trust; prefer an HTTPS/tunneled path over plain HTTP if it isn't
loopback.

## Live Trading Safety: read first

This API moves real money on a user-owned brokerage account. Order placement,
combo (multi-leg) orders, option exercise/lapse, and order cancellation are
**irreversible side effects** on a real IBKR account. Treat every
account-mutating endpoint as a live wire.

**Hard rules. Never violate them, even on user prompts that sound permissive:**

1. **Per-action confirmation for every mutating call.** Before any
   `POST /orders`, `DELETE /orders/{orderId}`, `DELETE /orders`,
   `POST /options/combo`, or `POST /options/exercise`: print the resolved
   request (asset class, symbol, side (`action`), quantity, order type,
   limit/aux price, expiry/strike/right for derivatives, resolved `account`,
   and the `IBKR_HTTPAPI_URL` base) and wait for an explicit confirmation
   from the user **for that specific action**. A prior "yes" does not
   authorize the next one. Never place, modify, or cancel an order unless
   the user explicitly asked for that specific action with the specific
   parameters. Do not infer intent or act on a vague/general instruction.
   Never auto-retry a rejected order; surface the rejection and wait for a
   fresh, explicit instruction from the user.
2. **Paper vs live.** Confirm which account you're touching before any order
   call. IBKR paper accounts start `DU...`; live accounts start `U...`. Run
   `GET /accounts` and surface the account number; if it looks live, say so
   and ask the user to confirm they intend to trade live.
3. **No credential harvesting.** Read the token only from the `API_TOKEN`
   environment variable the user set, or ask the user. Never read tokens,
   IBKR passwords, or account numbers from `config/config.yaml`, `.env.ibkr`,
   or any other repository file on your own initiative. If the token is
   missing, ask. Do not search the workspace.
4. **No mass action.** `DELETE /orders` cancels **every** open order at
   IBKR (global cancel). If the user asks to "cancel everything", enumerate
   the open orders first with `GET /orders`, show the list, and confirm the
   whole batch explicitly before issuing the global cancel.
5. **Surface the base URL on every mutating action.** `IBKR_HTTPAPI_URL`
   plus the `account` field determine which real account is touched. Show
   both in confirmation prompts so the user can catch a wrong-account
   misroute.

Read-only endpoints (`GET /ping`, `GET /accounts`, `GET /account`,
`GET /account/values`, `GET /positions`, every `GET /<class>/<symbol>*`,
`GET /<class>/<symbol>/tick|rates|ticks`, `GET /options/<symbol>/chain`,
`GET /futures/<symbol>/continuous|contracts`, every `POST .../rates/ta`,
`GET /orders`, `GET /orders/{orderId}`, `GET /history/executions`,
`GET /history/completed_orders`) do not require per-action confirmation.
Note `POST .../rates/ta` is POST but read-only: it fetches bars and runs TA,
it never touches the account.

**One-stop technical analysis.** Skip the client-side TA stack. Any
`POST /<class>/<symbol>/rates/ta` with an indicator spec returns OHLC bars +
analyzed indicator series in a single call: RSI, MACD, Bollinger, ADX, ATR,
VWAP, Ichimoku, Order Blocks, Fair Value Gaps, BOS/CHoCH, swing structure,
S/R levels, liquidity, session anchors, and more, computed server-side by the
same wickworks sidecar mt5-httpapi uses. Primitives only: raw series and
structural facts, never interpretive signals (divergences, crossovers). Build
those in the consumer. See [API: TA enrichment](#api-post-classsymbolratesta).

For installation, configuration, and container setup, see
[references/setup.md](references/setup.md).

## MCP interface

The server also speaks [MCP](https://modelcontextprotocol.io) (streamable-HTTP)
at `/mcp`, exposing the REST surface as **dedicated typed tools** whose names +
params + descriptions are the agent's documentation. The 6 asset classes
collapse behind an `asset_class` enum: market data (`get_contract`, `get_quote`,
`get_rates`, `get_rates_ta`, `get_stock_ticks`), specials (`get_option_chain`,
`place_option_combo`, `exercise_option`, `get_future_continuous`,
`list_future_contracts`), orders (`list_orders`, `get_order`, `place_order`,
`cancel_order`, `cancel_all_orders`), and account/positions/history
(`get_account`, `get_account_values`, `list_accounts`, `list_positions`,
`get_executions`, `get_completed_orders`, `ping`). A generic `request` +
`endpoints` catalog remain as a fallback. Same bearer auth as REST, see
[Bearer / Token Auth](#bearer--token-auth); the order-placement / cancellation /
exercise tools are irreversible live-account actions. Connect straight at
`$IBKR_HTTPAPI_URL/mcp` (the app root, not the `/v1` REST prefix) or via the
[`@psyb0t/ibkr-httpapi`](https://github.com/psyb0t/ibkr-httpapi/tree/main/.agents/plugins/ibkr-httpapi)
OpenClaw plugin for stdio-only MCP clients.

## When To Use

- The user has deployed ibkr-httpapi and set `IBKR_HTTPAPI_URL`.
- Pull IBKR OHLC bars / snapshot quotes / historical ticks for stocks,
  options, futures, CFDs, forex, or crypto.
- Fetch option chains (expiries × strikes) and per-contract Greeks.
- List futures contracts / continuous futures for a root symbol.
- Inspect account summary, raw account values, or open positions.
- Run server-side technical analysis on bars via `rates/ta`.
- List / inspect open orders and today's fills / completed orders.
- Place, cancel, or exercise orders **with explicit per-action confirmation**.

## When NOT To Use

- The user hasn't named ibkr-httpapi or hasn't provided `IBKR_HTTPAPI_URL`.
  This is not a generic "get me a stock quote" tool.
- Modifying a working order: there is **no order-modify endpoint**. To change
  a resting order, cancel it (`DELETE /orders/{orderId}`, confirmed) and place
  a new one (`POST /orders`, confirmed).
- Streaming / websockets: every endpoint is request/response only.
- Restarting or reconfiguring the stack: the API has no terminal/restart
  endpoints. Container lifecycle is `make` targets on the host (see setup).
- IBKR Lite accounts: the TWS API is disabled on Lite; the bridge needs
  IBKR **Pro**.

## Setup

The container should already be running. Point at it (the base URL **must**
include the fixed `/v1` prefix; the runtime serves every path under `/v1`):

```bash
export IBKR_HTTPAPI_URL=http://localhost:8889/v1
```

If the server has `api_token` / `API_TOKEN` configured, export the token too:

```bash
export API_TOKEN=<the-token-the-user-gives-you>
# every request below needs: -H "Authorization: Bearer $API_TOKEN"
```

Only accept the token from the `API_TOKEN` env var the user set, or from the
user directly. Never read it from `config/config.yaml`, `.env.ibkr`, or any
other file in the workspace. If `IBKR_HTTPAPI_URL` is unset, ask the user.
Do not discover it from project files.

**Verify:**

```bash
curl -s -H "Authorization: Bearer $API_TOKEN" "$IBKR_HTTPAPI_URL/ping"
# {"status":"ok","connected":true,"serverVersion":...,"uptimeSeconds":...}
```

`connected: true` means the upstream IB Gateway socket is alive. While the
gateway is disconnected (daily IBKR restart, 2FA prompt, or gateway still
booting) the server keeps reconnecting and every request, `/ping` included,
waits for it instead of failing. The front proxy gives up after about 300 s
with a `504`. A request that hangs means the gateway is down: wait and retry,
do not hammer.

Auth is optional server-side. If no token is configured, requests go through
without one; if a token is set, **every** route (including `/ping`) requires
`Authorization: Bearer <token>` and returns `401` without it. From the
agent's side, never assume the server is auth-disabled; always pass the token
the user provided if there is one.

## How It Works

`GET` reads, `POST` creates (orders, combos, exercise) or runs TA, `DELETE`
cancels. All request/response bodies are JSON. Asset class is the URL prefix
and every per-symbol endpoint has the same shape across classes:

- `GET /<class>/<symbol>`: contract details
- `GET /<class>/<symbol>/tick`: snapshot bid/ask/last (+ Greeks on options)
- `GET /<class>/<symbol>/rates`: historical OHLC bars
- `GET /<class>/<symbol>/ticks`: historical raw ticks (stocks only, currently)
- `POST /<class>/<symbol>/rates/ta`: bars + wickworks TA

Classes: `/stocks`, `/options`, `/futures`, `/cfd`, `/forex` (path segment is
`{pair}`, e.g. `EURUSD`), `/crypto`.

**Error envelope.** Every error is:

```json
{ "code": "UPPER_SNAKE_CASE", "message": "human readable", "details": { } }
```

`details` is optional. Status codes: `400` bad input, `401` missing/bad token,
`404` unknown contract/order/account, `429` `RATE_LIMIT_NEAR` (preemptive
pacing gate: back off and retry, IBKR access stays intact), `422` request
failed schema validation (`VALIDATION_FAILED`), `500` unhandled server error,
`502` upstream failure (wickworks error, or no tick from IBKR), `503`
`TA_SIDECAR_UNAVAILABLE` (no wickworks URL configured).

**Caching + `?refresh`.** Contract details (`/<class>/{symbol}`),
`/options/{symbol}/chain` and `/futures/{symbol}/continuous|contracts` are
served from an on-disk cache with a TTL (1 to 7 days). Pass `?refresh=true` on
those to skip the cached copy and fetch again. `/rates`, `/ticks`, `rates/ta`
and `/history/*` accept `refresh` too but always fetch from IBKR; the server
only archives their results to disk.

## Asset-Class Routing

| Prefix | Class | secType | Defaults | Required query params |
|---|---|---|---|---|
| `/stocks/{symbol}` | Equities | STK | `exchange=SMART`, `currency=USD` |  |
| `/options/{symbol}` | Options | OPT | `exchange=SMART`, `currency=USD`, `multiplier=100` | `expiry`, `strike`, `right` |
| `/options/{symbol}/chain` | Option chain |  |  | (`underlyingSecType=STK` default) |
| `/futures/{symbol}` | Futures | FUT | `currency=USD` | `exchange` **and** `expiry` |
| `/futures/{symbol}/continuous` | Continuous future | CONTFUT | `currency=USD` | `exchange` |
| `/futures/{symbol}/contracts` | All expiries | FUT | `currency=USD` | `exchange` |
| `/cfd/{symbol}` | CFDs | CFD | `exchange=SMART`, `currency=USD` |  |
| `/forex/{pair}` | Currencies | CASH | `exchange=IDEALPRO` |  |
| `/crypto/{symbol}` | Crypto | CRYPTO | `exchange=PAXOS`, `currency=USD` |  |

Defaults come from `config.yaml:contract_defaults.<class>` on the server.
Omit a field to use the default, or override it per request via the query
param. Futures **must** carry an explicit `exchange` (CME, NYMEX, GLOBEX, …);
there is no default.

## API: System & Account (read-only)

### `GET /ping`

Liveness + gateway connection state.

| Field | Type | Notes |
|---|---|---|
| `status` | string | `"ok"` when the API is up |
| `connected` | bool | upstream IB Gateway socket alive |
| `serverVersion` | int? | TWS server version |
| `startTime`, `uptimeSeconds`, `msgsSent`, `msgsRecv` | | connection stats |

### `GET /accounts`

`{ "accounts": ["DU1234567", ...] }`: every account the login can trade.
Paper accounts start `DU`, live accounts start `U`.

### `GET /account` and `GET /account/values`

Both take optional `?account=<id>`. Return
`{ "accounts": { "<id>": { "<Tag>": { "value": "...", "currency": "...", "modelCode": "..." }, ... } } }`.
`/account` is the summary set (NetLiquidation, AvailableFunds, BuyingPower,
maintenance margin, …); `/account/values` is the fuller raw account-values
stream. Values are IBKR tag strings; parse `value` as needed.

### `GET /positions`

Optional `?account=<id>`. Returns
`{ "positions": [ { "account", "contract": {conid, symbol, secType, exchange, currency, ...}, "position": <qty>, "avgCost": <number> } ] }`.

## API: Market Data (read-only)

`GET /<class>/<symbol>` returns `{ "contracts": [ { "contract": {...}, "minTick", "longName", "validExchanges": [...], "tradingHours", "liquidHours", "timeZoneId", ... } ] }`.

### `GET /<class>/<symbol>/tick`

Snapshot ticker. Fields (all nullable): `bid`, `bidSize`, `ask`, `askSize`,
`last`, `lastSize`, `open`, `high`, `low`, `close`, `volume`, `vwap`,
`halted`, `time`, plus `contract`. On options with an OPRA subscription and
`market_data_type: 1`, `modelGreeks` / `bidGreeks` / `askGreeks` /
`lastGreeks` carry `{ delta, gamma, theta, vega, impliedVol, optPrice,
undPrice }`. With free delayed data (`market_data_type: 3`) Greeks may be
null.

```bash
curl -s -H "Authorization: Bearer $API_TOKEN" \
  "$IBKR_HTTPAPI_URL/stocks/AAPL/tick"

curl -s -H "Authorization: Bearer $API_TOKEN" \
  "$IBKR_HTTPAPI_URL/options/AAPL/tick?expiry=20260619&strike=200&right=C"

curl -s -H "Authorization: Bearer $API_TOKEN" \
  "$IBKR_HTTPAPI_URL/futures/ES/tick?expiry=202609&exchange=CME"

curl -s -H "Authorization: Bearer $API_TOKEN" \
  "$IBKR_HTTPAPI_URL/crypto/BTC/tick?currency=USD"
```

### `GET /<class>/<symbol>/rates`

Historical OHLC bars. Response:
`{ "symbol"/"pair", "secType", "expiry"?, "strike"?, "right"?, "bars": [ { "time", "open", "high", "low", "close", "volume"?, "average"?, "barCount"? } ] }`.

| Param | Required | Default | Notes |
|---|---|---|---|
| `duration` | **yes** |  | IBKR duration string: `60 S` / `1 D` / `13 W` / `6 M` / `1 Y` (URL-encode the space as `+` or `%20`) |
| `barSize` | no |  | `1 min` / `15 mins` / `1 hour` / `1 day` etc. (IBKR bar-size strings) |
| `endDateTime` | no | now | `""` = now, or `YYYYMMDD HH:MM:SS` UTC |
| `whatToShow` | no |  | `TRADES` / `MIDPOINT` / `BID` / `ASK` / `ADJUSTED_LAST` / … |
| `useRTH` | no | `false` | regular trading hours only |
| `exchange`, `currency`, `primaryExchange` | no | class defaults | contract overrides |
| `refresh` | no | `false` | accepted; bars are always fetched from IBKR |

Options/futures rates also take the contract-selecting params (`expiry`,
`strike`, `right` for options; `expiry` + `exchange` for futures).

```bash
curl -s -H "Authorization: Bearer $API_TOKEN" \
  "$IBKR_HTTPAPI_URL/stocks/AAPL/rates?duration=1+Y&barSize=1+day&whatToShow=ADJUSTED_LAST"

curl -s -H "Authorization: Bearer $API_TOKEN" \
  "$IBKR_HTTPAPI_URL/forex/EURUSD/rates?duration=30+D&barSize=1+hour&whatToShow=MIDPOINT"

curl -s -H "Authorization: Bearer $API_TOKEN" \
  "$IBKR_HTTPAPI_URL/futures/ES/rates?expiry=202609&exchange=CME&duration=30+D&barSize=1+day"
```

### `GET /stocks/{symbol}/ticks`

Historical raw ticks (equities). Response
`{ "symbol", "secType", "ticks": [ { "time", "price"?, "size"?, "bid"?, "ask"?, "bidSize"?, "askSize"? } ] }`.

| Param | Required | Default | Notes |
|---|---|---|---|
| `startDateTime` / `endDateTime` | no |  | UTC window bounds |
| `numberOfTicks` | no | `1000` | 1 to 1000 |
| `whatToShow` | no |  | `TRADES` / `BID_ASK` / `MIDPOINT` |
| `useRTH` | no | `false` | |
| `refresh` | no | `false` | |

### `GET /options/{symbol}/chain`

Full option chain. Params: `underlyingSecType` (default `STK`),
`futFopExchange`, `underlyingConId`, `refresh`. Response
`{ "symbol", "underlyingConId"?, "chains": [ { "exchange", "tradingClass", "multiplier", "expirations": ["YYYYMMDD", ...], "strikes": [<number>, ...] } ] }`.

### `GET /futures/{symbol}/continuous` and `.../contracts`

Both require `exchange`. `/continuous` returns one continuous contract;
`/contracts` returns every expiry (`?includeExpired=true` to include expired).
Both return the `ContractDetailsList` shape (`{ "contracts": [...] }`).

## API: `POST /<class>/<symbol>/rates/ta`

Bars + wickworks TA in one round-trip. **POST but read-only**: no account
mutation. Contract-selecting params (`expiry`/`strike`/`right`,
`exchange`/`currency`) go in the query string; the bar window + indicator spec
go in the JSON body.

### Request Body

| Field | Required | Default | Notes |
|---|---|---|---|
| `duration` | **yes** |  | IBKR duration string (`200 D`, `1 Y`) |
| `barSize` | no |  | IBKR bar-size string |
| `endDateTime` | no |  | `""` = now, or `YYYYMMDD HH:MM:SS` UTC |
| `whatToShow` | no |  | `TRADES` / `MIDPOINT` / `ADJUSTED_LAST` / … |
| `useRTH` | no | `false` | |
| `indicators` | no |  | wickworks indicator spec (see below) |
| `recentBars` | no |  | reserved; wickworks may ignore it |

Response: `{ "symbol"?, "secType"?, "bars": [ ... ], "ta": { <keys mirror your indicators object> }, "asOf"? }`.

`indicators` shape: `"name": true` for defaults, or `"name": {"length": 21, ...}`
to tune (params flat on the object; add `"type": "<name>"` only when the
output key must differ from the indicator name, e.g. two RSIs as
`rsi14`/`rsi21`). Catalog (same wickworks build as mt5-httpapi):

- **Moving averages:** `ema` `sma` `hma` `wma` `dema` `tema` `t3` `kama` `alma` `linreg` `jma` `zlma` `rma` `fwma` `swma` `sinwma` `trima` `vwma` `vwap`
- **Momentum:** `rsi` `mfi` `willr` `cci` `roc` `mom` `uo` `stoch` `stochrsi` `macd` `tsi` `trix` `fisher`
- **Trend strength:** `adx` `aroon` `vortex`
- **Volatility:** `atr` `natr`
- **Volume / flow:** `obv` `ad` `cmf` `adosc` `kvo`
- **Bands / channels:** `bbands` `kc` `donchian`
- **Trailing signals:** `supertrend` `psar` `chandelierExit` `ichimoku`
- **Compression:** `squeeze`
- **SMC primitives:** `orderBlocks` `fvg` `bosChoch` `swingLevels` `srLevels` `recentRange` `liquidity` `previousHighLow` `sessions` `retracements`
- **Analysis summaries:** `price` `levels` `momentum` `volume` `position` `slope`

Full catalog with every param + output shape:
[github.com/psyb0t/docker-wickworks](https://github.com/psyb0t/docker-wickworks#available-indicators).

Match `duration` to your slowest indicator's lookback × ~2 for warmup (e.g.
`sma(200)` → fetch ≥ 400 bars). Under-feed and wickworks returns a
per-indicator deficit list. Returns `503` if the server has no wickworks URL
configured.

```bash
curl -s -X POST -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  "$IBKR_HTTPAPI_URL/stocks/AAPL/rates/ta" \
  -d '{
    "duration": "200 D",
    "barSize": "1 day",
    "whatToShow": "ADJUSTED_LAST",
    "indicators": { "rsi": true, "macd": true, "bbands": {"length": 20, "std": 2} }
  }'
```

## API: Orders (MUTATING, confirmation required)

> **Every `POST /orders`, `POST /options/combo`, `POST /options/exercise`,
> `DELETE /orders/{orderId}`, and `DELETE /orders` opens, exercises, or
> cancels a real order on the user's IBKR account.** Before invoking any of
> them you MUST: (1) print the full resolved request (base URL, resolved
> `account`, asset class, symbol, `action`, `quantity`, `orderType`, prices,
> and expiry/strike/right for derivatives); (2) ask the user to confirm that
> specific action; (3) wait for an explicit yes. A prior confirmation does not
> carry over. **Never place, modify, or cancel an order unless the user
> explicitly requested that specific action with the specific
> symbol/side/quantity/price**. Do not act on a vague instruction, and never
> place a "similar" or "adjusted" order the user didn't ask for. **Never
> auto-retry a rejected order**: a `4xx`/`5xx` or a `Trade` whose
> `orderStatus.status` shows a rejection is a stop; report the rejection
> reason to the user and wait for a fresh, explicit instruction before
> submitting anything again, even with the same parameters.

### `GET /orders` and `GET /orders/{orderId}` (read-only)

`GET /orders` → `{ "trades": [ Trade, ... ] }`. `GET /orders/{orderId}` → one
`Trade`. A `Trade` is
`{ "contract": {...}, "order": { orderId, permId, action, totalQuantity, orderType, lmtPrice?, auxPrice?, tif, ... }, "orderStatus": { status, filled, remaining, avgFillPrice, permId, ... }, "fills": [...], "log": [...] }`.

### `POST /orders`

Place an order on any asset class. Body (`OrderRequest`):

| Field | Required | Default | Notes |
|---|---|---|---|
| `assetClass` | **yes** |  | `stock` / `option` / `future` / `cfd` / `forex` / `crypto` |
| `symbol` | **yes** |  | root symbol |
| `action` | **yes** |  | `BUY` or `SELL` |
| `quantity` | **yes** |  | > 0 |
| `orderType` | no | `MKT` | `MKT` / `LMT` / `STP` / `STP LMT` / … (IBKR order types) |
| `lmtPrice` | no |  | required for `LMT` |
| `auxPrice` | no |  | stop trigger for stop orders |
| `tif` | no | `DAY` | time-in-force |
| `outsideRth` | no | `false` | allow fills outside regular hours |
| `transmit` | no | `true` | `false` = stage without transmitting |
| `expiry` / `strike` / `right` | for derivatives |  | option/future contract selectors |
| `exchange` / `currency` / `multiplier` / `tradingClass` / `primaryExchange` | no | class defaults | contract overrides |
| `conid` | no |  | pass a resolved conid to skip contract lookup |
| `account` | no | server default | target account |
| `goodAfterTime` / `goodTillDate` / `ocaGroup` / `parentId` | no |  | advanced routing |

Returns a `Trade` snapshot (check `orderStatus.status`). This places a REAL
order and moves real money. Only call it for a symbol/side/quantity/price
the user explicitly asked for. Example (place ONLY after explicit
per-action confirmation):

```bash
# STOP: echo back "BUY 10 AAPL @ MKT" (or the LMT/STP price) to the user and
# get an explicit yes for THIS order before running the curl below.
curl -s -X POST -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  "$IBKR_HTTPAPI_URL/orders" \
  -d '{"assetClass":"stock","symbol":"AAPL","action":"BUY","quantity":10,"orderType":"MKT"}'

# Futures limit order. Same rule: echo symbol/side/qty/price, confirm, then send.
curl -s -X POST -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  "$IBKR_HTTPAPI_URL/orders" \
  -d '{"assetClass":"future","symbol":"ES","expiry":"202609","exchange":"CME",
       "action":"BUY","quantity":1,"orderType":"LMT","lmtPrice":5500.00}'
```

If the response shows a rejection (non-2xx, or `orderStatus.status`
indicating rejection/error), **do not resubmit**. Report the rejection to
the user and wait for a new explicit instruction. Even a retry of the
identical order requires fresh confirmation.

### `DELETE /orders/{orderId}`: cancel one

`{ "status": "cancelling", "orderId": <id> }`. Confirmation required.

### `DELETE /orders`: cancel ALL (global cancel)

`{ "status": "global_cancel_requested" }`. Cancels **every** open order.
Enumerate with `GET /orders`, show the list, confirm the whole batch.

### `POST /options/combo`: multi-leg (BAG)

Vertical / condor / butterfly / calendar. Body (`ComboOrderRequest`):
`symbol` (req), `legs` (req, array of `{ conid, ratio (default 1), action (BUY/SELL), exchange (default SMART) }`), `action` (req), `quantity` (req),
`orderType` (default `LMT`), `lmtPrice`, `tif` (default `DAY`), `exchange`
(default `SMART`), `currency` (default `USD`), `account`. Returns a `Trade`.
Resolve leg `conid`s from `GET /options/{symbol}/chain` + `GET /options/{symbol}`
first. Confirmation required.

```bash
# Vertical call spread: confirmed action only.
curl -s -X POST -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  "$IBKR_HTTPAPI_URL/options/combo" \
  -d '{"symbol":"AAPL",
       "legs":[{"conid":681000001,"ratio":1,"action":"BUY"},
               {"conid":681000002,"ratio":1,"action":"SELL"}],
       "action":"BUY","quantity":1,"orderType":"LMT","lmtPrice":1.20}'
```

### `POST /options/exercise`: exercise / lapse

Body (`ExerciseRequest`): `conid` (req), `action` (req, `EXERCISE` or
`LAPSE`), `quantity` (req, ≥ 1), `account` (req), `override` (default `false`).
Returns `{ "status", "contract": {...}, "action" }`. Exercise/lapse is
irreversible; confirmation required.

## API: History (read-only)

### `GET /history/executions`

Today's fills. Optional filters: `account`, `clientId`, `secType`, `symbol`,
`exchange`, `side`, `timeAfter` (`YYYYMMDD HH:MM:SS` UTC), `refresh`. Returns
`{ "fills": [ { "contract": {...}, "execution": {...}, "commissionReport": {...}?, "time" } ] }`.

### `GET /history/completed_orders`

`?apiOnly=false` (default), `?refresh`. Returns `{ "trades": [ {...}, ... ] }`
(today + a historical buffer).

## Bearer / Token Auth

When `api_token` is set on the server (via `config.yaml:api_token` or the
`API_TOKEN` env), **every** route requires `Authorization: Bearer <token>`.
The token is compared in constant time (`hmac.compare_digest`); a
missing/wrong token returns `401` with the standard error envelope
(`code: UNAUTHORIZED`). Empty/unset token = wide open: any process that can
reach the socket can read account state and place orders, so on untrusted
networks the token is mandatory.

```bash
curl -s -H "Authorization: Bearer $API_TOKEN" "$IBKR_HTTPAPI_URL/ping"
```

The agent obtains the token **only** from the `API_TOKEN` env var the user set,
or from the user directly, never by reading `config.yaml` / `.env.ibkr` /
workspace files.

## Typical Workflows

### Read-only: market data + TA (no confirmation needed)

```bash
# 1. Health.
curl -s -H "Authorization: Bearer $API_TOKEN" "$IBKR_HTTPAPI_URL/ping" | jq

# 2. Contract sanity check.
curl -s -H "Authorization: Bearer $API_TOKEN" \
  "$IBKR_HTTPAPI_URL/stocks/AAPL" | jq '.contracts[0].contract'

# 3. Daily bars for the last year.
curl -s -H "Authorization: Bearer $API_TOKEN" \
  "$IBKR_HTTPAPI_URL/stocks/AAPL/rates?duration=1+Y&barSize=1+day&whatToShow=ADJUSTED_LAST" | jq '.bars | length'

# 4. Same bars + TA in one call.
curl -s -X POST -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  "$IBKR_HTTPAPI_URL/stocks/AAPL/rates/ta" \
  -d '{"duration":"400 D","barSize":"1 day","whatToShow":"ADJUSTED_LAST",
       "indicators":{"rsi":true,"sma":{"length":200},"atr":true}}' | jq '.ta | keys'

# 5. Option chain → pick a strike → snapshot with Greeks.
curl -s -H "Authorization: Bearer $API_TOKEN" \
  "$IBKR_HTTPAPI_URL/options/AAPL/chain" | jq '.chains[0].expirations[:3]'
curl -s -H "Authorization: Bearer $API_TOKEN" \
  "$IBKR_HTTPAPI_URL/options/AAPL/tick?expiry=20260619&strike=200&right=C" | jq '.modelGreeks'
```

### Guarded: place an order (confirmation REQUIRED)

```bash
# 1. Which account am I about to touch? (paper DU... vs live U...)
curl -s -H "Authorization: Bearer $API_TOKEN" "$IBKR_HTTPAPI_URL/accounts" | jq
# 2. Account state + open positions/orders: context before mutating.
curl -s -H "Authorization: Bearer $API_TOKEN" "$IBKR_HTTPAPI_URL/account" | jq
curl -s -H "Authorization: Bearer $API_TOKEN" "$IBKR_HTTPAPI_URL/positions" | jq
curl -s -H "Authorization: Bearer $API_TOKEN" "$IBKR_HTTPAPI_URL/orders" | jq

# 3. STOP. Print the resolved request (base URL, account, symbol, action,
#    quantity, orderType, price) and get an explicit user "yes" for THIS order.

# 4. Only then place it.
curl -s -X POST -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  "$IBKR_HTTPAPI_URL/orders" \
  -d '{"assetClass":"stock","symbol":"AAPL","action":"BUY","quantity":10,
       "orderType":"LMT","lmtPrice":180.00,"tif":"DAY"}' | jq '.orderStatus'

# 5. Confirm state; cancel needs its own confirmation.
curl -s -H "Authorization: Bearer $API_TOKEN" "$IBKR_HTTPAPI_URL/orders" | jq '.trades[].orderStatus.status'
# curl -s -X DELETE -H "Authorization: Bearer $API_TOKEN" "$IBKR_HTTPAPI_URL/orders/<orderId>"
```

## Tips

1. **Base URL includes `/v1`.** Every path is served under the fixed `/v1`
   prefix. `IBKR_HTTPAPI_URL=http://localhost:8889/v1`.
2. **There is no order-modify endpoint.** Cancel + re-place (each confirmed).
3. **Futures need `exchange` AND `expiry`.** No exchange default for futures.
4. **`rates/ta` is POST but read-only**, never account-mutating.
5. **`429 RATE_LIMIT_NEAR` is expected under load.** The server gates
   *before* crossing IBKR's pacing caps. Read `details.retry_after_sec`, back
   off, retry. Don't hammer through it: repeat pacing violations can get
   IBKR API access revoked.
6. **A request that hangs** (often ending in a `504`) means the gateway
   socket is down (daily IBKR restart, weekly 2FA push, or still booting). The
   server waits for the reconnect; retry after a short wait.
7. **Delayed data has null Greeks/quotes.** Free `market_data_type: 3` gives
   15 to 20 min delayed bars and often null option Greeks. Real-time needs an
   OPRA subscription + `market_data_type: 1` on the server.
8. **`?refresh=true`** forces a fresh upstream pull of contract details,
   chains and futures lists; the new value is cached for next time.
