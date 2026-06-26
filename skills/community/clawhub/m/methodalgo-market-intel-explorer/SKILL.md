---
name: methodalgo-market-intel-explorer
version: 1.4.2
description: >
  Fetch MethodAlgo crypto market intelligence with methodalgo-cli. Use when:
  checking crypto news, trading signals, token unlocks, ETF flows, chart
  snapshots, economic calendar events, macro data, BTC/ETH dominance, total
  crypto market cap, Fear & Greed, Altseason Index, or Binance public
  spot/futures prices, ticker, movers, order books, trades, klines, funding, OI,
  long/short sentiment, basis, exchange-info, and allowlisted raw endpoints.
metadata:
  openclaw:
    requires:
      env:
        - METHODALGO_API_KEY
      bins:
        - methodalgo
      anyBins:
        - node
        - npm
    primaryEnv: METHODALGO_API_KEY
    install:
      - kind: node
        package: methodalgo-cli
        bins: [methodalgo]
    homepage: https://github.com/methodalgo/methodalgo-market-intel-explorer
category: data-provider
credentials:
  METHODALGO_API_KEY:
    description: API key for the MethodAlgo service. Obtain one at https://account.methodalgo.com/account/api-keys
    required: true
provenance:
  cli: https://www.npmjs.com/package/methodalgo-cli
  minCliVersion: 1.0.36
  source: https://github.com/methodalgo/methodalgo-market-intel-explorer
  registry: https://clawhub.ai/methodalgo/methodalgo-market-intel-explorer
---

# MethodAlgo Market Intel Explorer Skill

Use this skill as the AI-facing routing layer for `methodalgo-cli`. Keep direct CLI calls in JSON mode unless the user explicitly asks for human-readable output.

## Install And Auth

Install or update the CLI:

```bash
npm install -g methodalgo-cli
methodalgo --version
```

Use `methodalgo-cli >= 1.0.36` for `macro` and `totals`; use `>= 1.0.26` for Binance public market data.

Most MethodAlgo service commands require `METHODALGO_API_KEY` or `methodalgo login`:

```bash
methodalgo login
```

Authentication rules:

- `news`, `signals`, `snapshot`, `calendar`, `macro`, and `totals` require MethodAlgo service access.
- `METHODALGO_API_KEY` is required for normal MethodAlgo CLI service usage and login flows.
- `methodalgo binance ...` uses Binance public endpoints and does not require a MethodAlgo API key or Binance API key.
- The CLI prioritizes `METHODALGO_API_KEY` over local login config.

Troubleshooting:

| Error | Action |
|---|---|
| Authentication Required / 401 / 403 | Set `METHODALGO_API_KEY`, run `methodalgo login`, or verify the key at `https://account.methodalgo.com/account/api-keys`. |
| `methodalgo` not found | Install with `npm install -g methodalgo-cli`. |
| `macro` / `totals` missing | Update to `methodalgo-cli >= 1.0.36`. |
| Binance command missing | Update to `methodalgo-cli >= 1.0.26`. |
| Network timeout / `fred request failed` | Check access to `methodalgo.com`, upstream macro/FRED services, or Binance public API endpoints. |

## Reference Loading

Load only the reference needed for the task:

- [references/command-reference.md](./references/command-reference.md): full parameter tables and command catalog for snapshot, news, calendar, macro, totals, and Binance.
- [references/signal-channels.md](./references/signal-channels.md): channel mechanisms and detailed `details` field meanings.
- [references/sample-output.md](./references/sample-output.md): compact JSON shapes for parsing and response validation.
- [references/output-shape-catalog.md](./references/output-shape-catalog.md): field-level output shape catalog for command variants.
- [references/ai-prompts.md](./references/ai-prompts.md): scenario templates for daily reports, symbol scans, liquidation monitoring, macro analysis, and Binance scans.

## Command Index

Always include `--json` for structured output.

```bash
methodalgo news --type <article|breaking|onchain|report> --limit <N> --json
methodalgo news --type article --search "Bitcoin" --limit 5 --json
methodalgo signals <channel> --limit <N> --json
methodalgo snapshot <symbol> [tf] --url --json
methodalgo calendar --countries <codes> [options] --json
methodalgo macro <subcommand> [options] --json
methodalgo totals [metric] [options] --json
methodalgo binance <subcommand> [options] --json
```

Core routing:

| Intent | Prefer |
|---|---|
| Latest market news | `methodalgo news --type breaking --limit 50 --json` |
| Deep market articles | `methodalgo news --type article --limit 100 --json` |
| Symbol-specific news | `methodalgo news --type article --search "<symbol or name>" --limit 10 --json` |
| Trading signals | `methodalgo signals <channel> --limit 10 --json` |
| Chart image URL | `methodalgo snapshot BTCUSDT.P 60 --url --json` |
| Economic events | `methodalgo calendar --countries US,EU,CN --json` |
| Macro dashboard | `methodalgo macro dashboard --json` |
| Net liquidity | `methodalgo macro liquidity --tail 52 --json` |
| Crypto-wide totals | `methodalgo totals --json` |
| BTC dominance / Fear & Greed / Altseason | `methodalgo totals <metric> --history 30d|90d|1y --json` |
| Binance spot price | `methodalgo binance price BTCUSDT --json` |
| Binance futures price | `methodalgo binance price BTCUSDT.P --json` |
| Binance futures funding / OI / sentiment | `methodalgo binance funding BTCUSDT.P --json`; `methodalgo binance oi BTCUSDT.P --period 5m --json`; `methodalgo binance sentiment BTCUSDT.P --period 5m --json` |

## Signals Schema Lock

Use `methodalgo signals <channel> --limit <N> --json`.

Standard signal channels return an array of message objects. Each message may contain `id`, `timestamp`, `attachments`, `image`, and a nested `signals` array. Each nested signal may contain `title`, `description`, `direction`, and channel-specific `details`. Full examples live in [references/sample-output.md](./references/sample-output.md).

Protected `details` field map:

| Channel | Required `details` fields |
|---|---|
| `breakout-*` | `Symbol`, `TimeFrame`, `Type` (`UP` / `DOWN`), `BreakPrice`, `Exchange` |
| `liquidation` | `Symbol`, `Side`, `Quantity`, `Average Price`, `Liquidation Price`, `Position Total` |
| `exhaustion-*` | `Type`, `Timeframe`, `Exhaustion Side`, `Safety`, `Tip`, `Exchange` |
| `golden-pit-*` | `Pattern`, `Safety` |
| `etf-tracker` | `Net Inflow`, `7 Days Avg.` |
| `market-today` | Variable Discord-style summary fields; do not use it as the structured metric source. |

Signal interpretation:

- `exhaustion-buyer` is bearish buyer exhaustion.
- `exhaustion-seller` is bullish seller exhaustion.
- If CLI help text conflicts with these exhaustion directions, follow this Schema Lock.
- `market-today` is a Discord-style summary stream. For structured BTC Dominance, ETH Dominance, Total Market Cap, Fear & Greed, and Altseason Index values, call `methodalgo totals --json` or `methodalgo totals <metric> --json`.

`token-unlock` is the special-case channel: it returns a root object shaped as `{ signals: [...], updatedAt }`, not a root array. Token unlock items include `ts`, `symbol`, `perc`, `progress`, `circSup`, `countDown`, `marketCap`, `unlockToken`, and `unlockTokenVal`. When showing countdowns, calculate live timing from `ts` and `updatedAt` rather than trusting `countDown` as immutable text.

## Market Data Rules

News:

- `article` normally includes richer `excerpt`, `analysis`, and `url`.
- `breaking`, `onchain`, and `report` can omit article-style fields.
- For Chinese output, prefer `title.zh`, `excerpt.zh`, and `analysis.zh` when present.
- News limit can be as high as 500; use 50-100 for broad time coverage.

Macro:

- Use `methodalgo macro ...` for server-side macro/FRED-derived data. The CLI no longer needs a local FRED key.
- `methodalgo macro liquidity` computes Net Liquidity from Fed Assets - RRP - TGA and is the default liquidity command for BTC macro analysis.
- Macro commands can still fail on upstream service/network errors such as `fred request failed`; surface the failure instead of fabricating macro values.
- For subcommand tables and high-alpha series IDs such as `FEDFUNDS`, `WALCL`, `M2SL`, `RRPONTSYD`, `WTREGEN`, `CPIAUCSL`, `DGS10`, `DGS2`, `REAINTRATREARAT10Y`, `DTWEXBGS`, and `VIXCLS`, read [references/command-reference.md](./references/command-reference.md).

Totals:

- Use `methodalgo totals --json` for crypto-wide structured metrics.
- Supported metrics include `btc-dominance`, `eth-dominance`, `total-market-cap`, `fear-greed`, and `altseason-index`.
- Plain `methodalgo totals` shows human CLI help; `methodalgo totals --json` is the AI structured aggregate endpoint.
- Use `signals market-today` only when the user wants the Discord-style market summary stream.

Binance:

- `BTCUSDT` means spot.
- `BTCUSDT.P` means USD-M perpetual futures; the CLI sends `BTCUSDT` to Binance futures APIs.
- Use `--market futures` for list-style futures queries such as `movers`.
- `funding`, `oi`, `sentiment`, and `basis` are futures-only.
- Binance `--json` often returns direct Binance API shapes; do not assume every subcommand has the same wrapper.
- `raw` is restricted to allowlisted public endpoints. Account, order, trading, signed, and user-data endpoints are intentionally blocked.

## Two-Phase Fetch Strategy

Use a low-cost preview first, then deepen only where the data points:

1. Preview: fetch 5-10 items for news, signals, totals, or Binance market data.
2. Deep dive: use `--after`, `--search`, symbol filtering, or larger limits after identifying relevant IDs, symbols, or themes.

Examples:

```bash
methodalgo signals breakout-mtf --limit 5 --json
methodalgo signals breakout-mtf --limit 100 --after "msgId" --json
methodalgo news --type article --search "SOL" --limit 10 --json
```

## Scenario Shortcuts

| Scenario | Commands |
|---|---|
| Daily market overview | `totals --json`; `signals etf-tracker`; `news article`; `news breaking`; optionally `signals market-today`. |
| Specific coin deep scan | Search news, inspect breakout signals, fetch Binance futures price/funding/OI/sentiment, then fetch snapshot. |
| Liquidation and reversal monitor | `signals liquidation`; `signals exhaustion-buyer`; `signals exhaustion-seller`. |
| Token unlock check | `signals token-unlock --limit 1 --json`; parse root `signals`. |
| Macro regime check | `macro dashboard`; `macro recession`; `macro liquidity --tail 52`; optional `macro compare` or `macro zscore`. |
| Binance microstructure | `binance price`; `binance klines`; `binance funding`; `binance oi`; `binance sentiment`. |

## Output Rules

- Parse JSON with structured logic, not string matching.
- Surface authentication and version errors explicitly.
- Do not collapse `market-today` and `totals`; they serve different data shapes.
- Do not normalize away `.P` when presenting user-facing futures symbols.
- If a task needs exact parameter choices, load [references/command-reference.md](./references/command-reference.md).
- If a task needs sample JSON, load [references/sample-output.md](./references/sample-output.md).
- If a task needs field coverage for less common command variants, load [references/output-shape-catalog.md](./references/output-shape-catalog.md).

Github: https://github.com/methodalgo/methodalgo-market-intel-explorer
ClawHub: https://clawhub.ai/methodalgo/methodalgo-market-intel-explorer
