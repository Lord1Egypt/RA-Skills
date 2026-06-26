# Command Reference

This file keeps full command syntax and parameter tables out of `SKILL.md` while preserving task-level detail.

## Snapshot

```bash
methodalgo snapshot <symbol> [tf] --url --json
```

| Parameter | Description | Example |
|---|---|---|
| `symbol` | Required trading pair. Use `.P` for USD-M perpetual futures. | `SOLUSDT`, `SOLUSDT.P` |
| `tf` | Optional timeframe. Default is `60`. | `15`, `30`, `60`, `240`, `D`, `W`, `M` |
| `--url` | Return a chart image URL instead of binary output. | `--url` |
| `--buffer` | Return raw binary image stream for programmatic processing. | `--buffer` |
| `--json` | Return structured JSON. | `--json` |

Typical output has `symbol`, `tf`, `url`, and `timestamp`.

## News

```bash
methodalgo news --type <type> --limit <N> --json
methodalgo news --type article --search "Bitcoin" --limit 5 --json
```

| Type | Description |
|---|---|
| `article` | Deep crypto market news and analysis, usually with summaries, analysis, and URL. |
| `breaking` | Real-time breaking news flashes. |
| `onchain` | On-chain anomaly monitoring. |
| `report` | Institutional research reports. |

| Parameter | Description | Example |
|---|---|---|
| `--type` | Required news type. | `--type breaking` |
| `--limit` | Number of results, up to 500. | `--limit 50` |
| `--language` | Language hint. | `--language zh`, `--language en` |
| `--search` | Search titles by keyword. | `--search "Bitcoin"` |
| `--start-date` | Start date. | `--start-date 2026-03-20` |
| `--end-date` | End date. | `--end-date 2026-03-30` |

## Signals

```bash
methodalgo signals <channel> --limit <N> --json
methodalgo signals <channel> --limit 100 --after "msgId" --json
```

| Channel | Description | Frequency |
|---|---|---|
| `breakout-htf` | High timeframe breakout, usually 1D/3D over a 100-candle rolling window. | Medium |
| `breakout-mtf` | Medium timeframe breakout, usually 1H/4H over a 100-candle rolling window. | High |
| `breakout-24h` | 24-hour rolling-window breakout detection. | Ultra-high |
| `liquidation` | Real-time large liquidation alerts. | Real-time |
| `exhaustion-seller` | Seller exhaustion reversal signal. This is bullish. | Low/Medium |
| `exhaustion-buyer` | Buyer exhaustion reversal signal. This is bearish. | Low/Medium |
| `golden-pit-mtf` | Medium timeframe Golden Pit, 30m/1h/4h. | Medium |
| `golden-pit-ltf` | Low timeframe Golden Pit, 5m/15m. | High |
| `token-unlock` | Token unlock events with unlock time, percentage, fundamentals, and value. | Daily |
| `etf-tracker` | Daily BTC/ETH/SOL/XRP ETF fund flow broadcasts. | Daily |
| `market-today` | Discord-style market summary stream; use `totals` for structured values. | Daily |

See `SKILL.md` for protected schema rules and `references/signal-channels.md` for mechanism detail.

## Calendar

```bash
methodalgo calendar --countries <codes> [options] --json
```

| Parameter | Description | Example |
|---|---|---|
| `--countries` | Required comma-separated ISO country codes. | `--countries US,EU,CN` |
| `--from` | Start date. Default is around two days ago. | `--from 2026-03-20` |
| `--to` | End date. Default is around two days later. | `--to 2026-03-30` |
| `--json` | Return structured JSON. | `--json` |

Typical event fields include `title`, `country`, `indicator`, `period`, `comment`, `actual`, `forecast`, `previous`, `importance`, `date`, `source`, and `source_url`.

## Macro

Use `methodalgo macro ...` for server-side macroeconomic data, FRED-derived indicators, economic calendar data, and market environment series. A local FRED key is not required.

```bash
methodalgo macro <subcommand> [options] --json
```

| Subcommand | Description | Example |
|---|---|---|
| `environment` | Current market environment data. | `methodalgo macro environment --json` |
| `history <metric>` | Historical market environment series. | `methodalgo macro history altcoinSeason --timeframe 90d --json` |
| `snapshot` | Server-side macro snapshot. | `methodalgo macro snapshot --json` |
| `series <source> <seriesId>` | Time series from a source such as FRED. | `methodalgo macro series fred DGS10 --timeframe 6m --json` |
| `calendar` | Server-side economic calendar. | `methodalgo macro calendar --countries US --json` |
| `dashboard` | Full macro overview across rates, inflation, liquidity, employment, and related data. | `methodalgo macro dashboard --json` |
| `recession` | Recession indicator scorecard. | `methodalgo macro recession --json` |
| `liquidity` | Net liquidity analysis using Fed Assets - RRP - TGA. | `methodalgo macro liquidity --tail 52 --json` |
| `get <id>` | Observation data for a specific macro series ID. | `methodalgo macro get FEDFUNDS --json` |
| `info <id>` | Metadata for a specific macro series ID. | `methodalgo macro info FEDFUNDS --json` |
| `latest <id>` | Latest value for a specific series ID. | `methodalgo macro latest FEDFUNDS --json` |
| `search <q>` | Search for FRED series by keywords. | `methodalgo macro search "gold price" --json` |
| `compare <ids>` | Compare multiple comma-separated series IDs. | `methodalgo macro compare DGS10,DGS2 --json` |
| `changes <id>` | Show recent changes and trends for a series. | `methodalgo macro changes WALCL --json` |
| `spread <series1> <series2>` | Compute difference between two series. | `methodalgo macro spread T10Y2Y T10Y3M --json` |
| `zscore <id>` | Z-score and percentile analysis vs historical data. | `methodalgo macro zscore CPIAUCSL --lookback 5y --json` |

High-alpha series IDs for crypto traders:

| Category | Series ID | Name | Typical relevance |
|---|---|---|---|
| Policy | `FEDFUNDS` | Fed Funds Rate | Baseline discount rate for risk assets. |
| Liquidity | `WALCL` | Fed Total Assets | Direct liquidity context for BTC. |
| Liquidity | `M2SL` | M2 Money Supply | Broad liquidity pool size. |
| Liquidity | `RRPONTSYD` | Reverse Repo | Higher readings can drain liquidity. |
| Liquidity | `WTREGEN` | Treasury General Account | Lower readings can release liquidity. |
| Inflation | `CPIAUCSL` | CPI, all items | Core inflation pressure for Fed policy. |
| Inflation | `PCEPILFE` | Core PCE | Fed-preferred inflation gauge. |
| Yields | `DGS10`, `DGS2` | 10Y / 2Y Treasury | Risk-free-rate pressure on BTC. |
| Real Rate | `REAINTRATREARAT10Y` | 10Y Real Interest Rate | Cost of money after inflation. |
| Currency | `DTWEXBGS` | Broad Dollar Index | Strong dollar usually pressures BTC. |
| Risk | `VIXCLS` | VIX | Stress and volatility context. |

Macro impact shortcuts:

| Indicator | Direction | Typical crypto impact |
|---|---|---|
| `FEDFUNDS`, `DGS10` | Rising | Bearish: higher cost of capital. |
| `CPIAUCSL`, `PCEPILFE` | Above target | Bearish: supports tighter Fed policy. |
| `macro liquidity` | Expanding | Bullish: more excess liquidity for risk assets. |
| `DTWEXBGS` | Strengthening | Bearish: stronger USD often pressures BTC. |
| `REAINTRATREARAT10Y` | Falling or negative | Bullish: supports non-yielding assets such as gold and BTC. |

| Parameter | Description | Example |
|---|---|---|
| `--tail` | Show only the last N observations where supported; `--tail 52` approximates one year of weekly liquidity data. | `--tail 52` |
| `--m2` | Include M2 context in liquidity output. | `--m2` |
| `--lookback` | Lookback window for `zscore`. | `--lookback 5y`, `24m`, `365d` |
| `--json` | Return structured JSON. | `--json` |

## Totals

Use `totals` for structured crypto market-wide statistics. Use `signals market-today` only for the Discord-style market summary stream.

```bash
methodalgo totals [metric] [options] --json
```

| Metric | Description | Example |
|---|---|---|
| `btc-dominance` | BTC dominance. | `methodalgo totals btc-dominance --history 90d --json` |
| `eth-dominance` | ETH dominance. | `methodalgo totals eth-dominance --json` |
| `total-market-cap` | Total crypto market capitalization. | `methodalgo totals total-market-cap --json` |
| `fear-greed` | Fear & Greed Index. | `methodalgo totals fear-greed --history 30d --json` |
| `altseason-index` | Altseason Index. | `methodalgo totals altseason-index --history 90d --json` |

| Parameter | Description | Example |
|---|---|---|
| `--convert` | Quote currency. Default is `USD`. | `--convert USD` |
| `--history` | Include history for `30d`, `90d`, or `1y`. | `--history 90d` |
| `--json` | Return structured JSON. | `--json` |

Plain `methodalgo totals` without `--json` shows available metric help for humans. `methodalgo totals --json` is the AI structured aggregate endpoint and returns all supported market-wide metrics in one response.

## Binance Public Market Data

```bash
methodalgo binance <subcommand> [options] --json
```

Symbol convention:

| Input | Market | Meaning |
|---|---|---|
| `BTCUSDT` | Spot | Binance spot symbol. |
| `BTCUSDT.P` | USD-M futures | Perpetual futures symbol; the CLI strips `.P` before calling futures APIs. |

`--market auto|spot|futures` is available where supported. `auto` uses `.P` to infer futures. List-style commands such as `ticker` and `movers` default to spot unless `--market futures` is provided.

| Subcommand | Description | Example |
|---|---|---|
| `price <symbol>` | Latest price, 24h change, high/low, and quote volume. | `methodalgo binance price BTCUSDT.P --json` |
| `ticker [symbol]` | 24h ticker stats for one symbol or high-volume USDT pairs. | `methodalgo binance ticker BTCUSDT --json` |
| `movers` | 24h gainers and losers for spot or futures. | `methodalgo binance movers --market futures --limit 10 --json` |
| `book <symbol>` | Order book depth. | `methodalgo binance book ETHUSDT.P --limit 20 --json` |
| `trades <symbol>` | Recent market trades. | `methodalgo binance trades SOLUSDT --limit 20 --json` |
| `klines <symbol>` | OHLCV candlesticks. | `methodalgo binance klines BTCUSDT.P --interval 15m --limit 100 --json` |
| `funding <symbol>` | USD-M futures funding rate and mark/index price. | `methodalgo binance funding BTCUSDT.P --limit 8 --json` |
| `oi <symbol>` | USD-M futures open interest and recent OI history. | `methodalgo binance oi BTCUSDT.P --period 5m --limit 12 --json` |
| `sentiment <symbol>` | USD-M futures long/short ratios and taker buy/sell ratio. | `methodalgo binance sentiment BTCUSDT.P --period 5m --limit 12 --json` |
| `basis <symbol>` | USD-M futures basis and basis rate. | `methodalgo binance basis BTCUSDT.P --period 5m --limit 12 --json` |
| `exchange-info [symbol]` | Symbol rules and exchange metadata. | `methodalgo binance exchange-info BTCUSDT.P --json` |
| `raw <path>` | Allowlisted public endpoint passthrough. | `methodalgo binance raw /fapi/v1/openInterest -p symbol=BTCUSDT --json` |

| Parameter | Description | Example |
|---|---|---|
| `--market` | `auto`, `spot`, or `futures` where supported. | `--market futures` |
| `--limit` | Number of rows or Binance request limit where supported. | `--limit 20` |
| `--interval` | Kline interval. | `--interval 15m` |
| `--period` | Futures statistics period. | `--period 5m`, `15m`, `1h`, `4h`, `1d` |
| `--min-volume` | Minimum quote volume for movers filtering. | `--min-volume 1000000` |
| `-p`, `--param` | Raw endpoint query parameter. | `-p symbol=BTCUSDT` |
| `--json` | Return JSON. | `--json` |

Parsing notes:

- `--json` usually returns the direct Binance API response.
- `ticker --limit` affects formatted table output; with `--json`, the raw Binance response is returned.
- `movers` returns normalized `{ market, gainers, losers, timestamp }`.
- `funding`, `oi`, `sentiment`, and `basis` are futures-only.
- `BTCUSDT` and `BTCUSDT.P` both resolve to `BTCUSDT` for futures-only commands.
- `raw` is restricted to allowlisted public endpoints; signed, account, order, trading, and user-data endpoints are blocked.
