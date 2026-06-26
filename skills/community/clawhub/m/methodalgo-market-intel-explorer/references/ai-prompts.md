# AI Prompt Templates

Use these scenario templates as command plans. Keep `--json` on all data calls and apply the two-phase flow: preview first, deepen only after symbols, IDs, or themes are clear.

## Daily Market Overview

```text
1. methodalgo totals --json
2. methodalgo signals etf-tracker --limit 10 --json
3. methodalgo news --type article --limit 50 --json
4. methodalgo news --type breaking --limit 50 --json
5. Optional: methodalgo signals market-today --limit 5 --json
```

Use `totals` for structured BTC dominance, ETH dominance, total market cap, Fear & Greed, and Altseason Index. Use `market-today` only for the Discord-style summary stream.

## Specific Coin Deep Scan

Replace `SOL` / `SOLUSDT.P` with the target asset.

```text
1. methodalgo news --type article --search "SOL" --limit 10 --json
2. methodalgo signals breakout-mtf --limit 200 --json
3. methodalgo binance price SOLUSDT.P --json
4. methodalgo binance funding SOLUSDT.P --json
5. methodalgo binance oi SOLUSDT.P --period 5m --limit 12 --json
6. methodalgo binance sentiment SOLUSDT.P --period 5m --limit 12 --json
7. methodalgo snapshot SOLUSDT.P 60 --url --json
```

Filter broad signal responses by symbol before drawing conclusions.

## Liquidation And Reversal Monitor

```text
1. methodalgo signals liquidation --limit 50 --json
2. methodalgo signals exhaustion-seller --limit 10 --json
3. methodalgo signals exhaustion-buyer --limit 10 --json
```

Interpretation: `exhaustion-seller` is bullish seller exhaustion; `exhaustion-buyer` is bearish buyer exhaustion.

## Token Unlock Alerts

```text
methodalgo signals token-unlock --limit 1 --json
```

Parse the root object as `{ signals: [...] }`, not as an array. Use `ts` and `updatedAt` for live countdown logic.

## Macro Analysis

```text
1. methodalgo macro dashboard --json
2. methodalgo macro recession --json
3. methodalgo macro liquidity --tail 52 --json
4. Optional: methodalgo macro compare DTWEXBGS,DGS10 --json
5. Optional: methodalgo macro zscore REAINTRATREARAT10Y --json
```

Use `macro liquidity` for Net Liquidity (Fed Assets - RRP - TGA). No local FRED key is required.

## Calendar Volatility Scan

```text
methodalgo calendar --countries US,EU,CN --json
```

Focus on high-importance events and compare `actual`, `forecast`, and `previous`.

## Binance Microstructure Scan

```text
1. methodalgo binance price BTCUSDT.P --json
2. methodalgo binance klines BTCUSDT.P --interval 15m --limit 100 --json
3. methodalgo binance funding BTCUSDT.P --json
4. methodalgo binance oi BTCUSDT.P --period 5m --limit 12 --json
5. methodalgo binance sentiment BTCUSDT.P --period 5m --limit 12 --json
```

`BTCUSDT` is spot; `BTCUSDT.P` is USD-M futures. For list-style futures commands, include `--market futures`.

## Movers Discovery

```text
1. methodalgo binance movers --market spot --limit 10 --json
2. methodalgo binance movers --market futures --limit 10 --json
3. For top movers: price + funding + oi + sentiment + snapshot.
```
