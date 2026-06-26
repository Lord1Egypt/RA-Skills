# Output Shape Catalog

Use this catalog when compact examples in `sample-output.md` are not enough. It preserves field-level coverage for command variants without loading long JSON fixtures into `SKILL.md`.

## News Shapes

| Command | Root shape | Important fields |
|---|---|---|
| `news --type article` | Array of items | `type`, `title.en`, `title.zh`, `excerpt.en`, `excerpt.zh`, `description`, `analysis`, `publish_date`, `url` |
| `news --type breaking` | Array of items | `type`, `title.en`, `title.zh`, `publish_date`, optional empty `url` |
| `news --type onchain` | Array of items | `type`, `title.en`, `title.zh`, `publish_date` |
| `news --type report` | Array of items | `type`, `title.en`, `title.zh`, `publish_date` |

Parsing note: do not assume `excerpt`, `analysis`, or `url` exists outside `article`.

## Signal Shapes

| Channel | Root shape | Nested shape | Protected fields |
|---|---|---|---|
| `breakout-*` | Array of message objects | `signals[]` | `details.Symbol`, `details.TimeFrame`, `details.Type`, `details.BreakPrice`, `details.Exchange` |
| `liquidation` | Array of message objects | `signals[]` | `details.Symbol`, `details.Side`, `details.Quantity`, `details.Average Price`, `details.Liquidation Price`, `details.Position Total` |
| `exhaustion-*` | Array of message objects | `signals[]` | `details.Type`, `details.Timeframe`, `details.Exhaustion Side`, `details.Safety`, `details.Tip`, `details.Exchange` |
| `golden-pit-*` | Array of message objects | `signals[]` | `details.Pattern`, `details.Safety` |
| `etf-tracker` | Array of message objects | `signals[]` | `details.Net Inflow`, `details.7 Days Avg.` |
| `market-today` | Array of message objects | `signals[]` | Variable Discord-style summary fields; use `totals` for structured market metrics. |
| `token-unlock` | Object | root `signals[]` | `ts`, `symbol`, `perc`, `progress`, `circSup`, `countDown`, `marketCap`, `unlockToken`, `unlockTokenVal`, root `updatedAt` |

Message object fields commonly include `id`, `timestamp`, `attachments`, `image`, and `signals`.

## Snapshot Shape

| Command | Root shape | Important fields |
|---|---|---|
| `snapshot <symbol> [tf] --url --json` | Object | `symbol`, `tf`, `url`, `timestamp` |

## Calendar Shape

| Command | Root shape | Important fields |
|---|---|---|
| `calendar --countries ... --json` | Array of events | `title`, `country`, `indicator`, `period`, `comment`, `actual`, `forecast`, `previous`, `importance`, `date`, `source`, `source_url` |

## Totals Shapes

| Command | Root shape | Important fields |
|---|---|---|
| `totals --json` | Object | `command`, `convert`, `source`, `updatedAt`, `metrics` object keyed by metric name |
| `totals <metric> --json` | Object | `metric`, `label`, `value`, `displayValue`, `raw`, metric-specific fields |
| `totals <metric> --history 30d|90d|1y --json` | Object with history | current metric fields plus historical points |

Supported metric IDs: `btc-dominance`, `eth-dominance`, `total-market-cap`, `fear-greed`, `altseason-index`.

## Macro Shapes

| Command | Root shape | Important fields |
|---|---|---|
| `macro dashboard --json` | Object | rates, inflation, liquidity, employment, and broad market environment sections |
| `macro recession --json` | Object | recession scorecard signals and summary values |
| `macro liquidity --json` | Object or upstream error | `series[]`, `netLiquidity`, `fedAssets`, `rrp`, `tga`, optional M2 context; may print `fred request failed` on upstream/network failure |
| `macro get <id> --json` | Object | requested series ID, observations, date/value rows, source metadata where available |
| `macro info <id> --json` | Object | requested series ID, title/name, units, frequency, source metadata where available |
| `macro latest <id> --json` | Object | series ID, latest observation, date, value |
| `macro zscore <id> --json` | Object | latest value, z-score, percentile, lookback |
| `macro compare <ids> --json` | Object | aligned series values for requested IDs |
| `macro spread <series1> <series2> --json` | Object | spread series, latest spread, source series IDs |
| `macro search <q> --json` | Array or object with results | matching series IDs, title/name, source metadata |
| `macro changes <id> --json` | Object | recent observations, change values, trend metadata |
| `macro series <source> <seriesId> --json` | Object | source, series ID, observations |

Important macro IDs: `FEDFUNDS`, `WALCL`, `M2SL`, `RRPONTSYD`, `WTREGEN`, `CPIAUCSL`, `PCEPILFE`, `DGS10`, `DGS2`, `REAINTRATREARAT10Y`, `DTWEXBGS`, `VIXCLS`.

## Binance Shapes

Binance `--json` usually returns direct Binance API response shapes except where the CLI explicitly normalizes the result.

| Command | Root shape | Important fields |
|---|---|---|
| `binance price <symbol> --json` | Object | `market`, `symbol`, `price`, `changePercent`, `quoteVolume`, `high`, `low`, `closeTime` |
| `binance ticker [symbol] --json` | Object or array from Binance ticker API | `symbol`, `priceChange`, `priceChangePercent`, `lastPrice`, `volume`, `quoteVolume` |
| `binance movers --json` | Normalized object | `market`, `gainers[]`, `losers[]`, ISO `timestamp`; rows include `symbol`, `pctChange`, `price`, `rawPrice`, `quoteVolume`, `volumeLabel`, `rankType`, `direction`, `openTime`, `closeTime` |
| `binance book <symbol> --json` | Object | `lastUpdateId`, `bids`, `asks` |
| `binance trades <symbol> --json` | Array | trade ID, `price`, `qty`, `quoteQty`, `time`, side flags where provided |
| `binance klines <symbol> --json` | Array of kline arrays or normalized rows | open time, `open`, `high`, `low`, `close`, `volume`, close time, quote volume |
| `binance funding <symbol> --json` | Object | `premium` object with `symbol`, `markPrice`, `indexPrice`, `lastFundingRate`, `interestRate`, `nextFundingTime`, `time`; `history[]` funding rows |
| `binance oi <symbol> --json` | Object | `current` object with `symbol`, `openInterest`, `time`; `history[]` rows with `sumOpenInterest`, `sumOpenInterestValue`, `timestamp` |
| `binance sentiment <symbol> --json` | Object | `globalRatio[]`, `topAccount[]`, `topPosition[]`, `taker[]`; rows include long/short ratios or taker buy/sell volume fields |
| `binance basis <symbol> --json` | Object or rows | basis, basis rate, index price, futures price, timestamp |
| `binance exchange-info [symbol] --json` | Object | symbol rules, filters, precision, status, contract metadata |
| `binance raw <path> -p key=value --json` | Direct allowlisted endpoint response | endpoint-specific public fields |

Futures-only commands: `funding`, `oi`, `sentiment`, `basis`. `BTCUSDT.P` is the user-facing USD-M futures convention; futures-only commands ultimately call Binance with `BTCUSDT`.
