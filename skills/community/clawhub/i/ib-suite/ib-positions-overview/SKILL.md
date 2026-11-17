---
name: ib-positions-overview
description: Read-only positions overview from Interactive Brokers. Use when the user asks to list every open position with its symbol, name, asset type, quantity, long/short, average cost, current price, market value, unrealized P&L and return, account weight, industry, market/country, and currency, or to rank positions by market value, profit, loss, or account weight and flag the most concentrated name. Reads position state only — never account cash detail, never orders.
metadata:
  openclaw:
    requires:
      bins: [python3]
      config: [config.yaml]
    os: [darwin, linux]
---

# ib-positions-overview

Read-only positions overview for the IB analyst toolchain. Answers "what do I
hold right now, and where is my capital and risk?" in one call: every open
position enriched into a full line, then ranked four ways with the single most
concentrated name flagged. This skill connects with `readonly=True` and only
reads; it NEVER places, modifies, or cancels an order.

## Prerequisites

Config and the shared venv are owned by the `ib-suite` index skill (see its
first-run setup). Start IB Gateway (paper on 4002 / live on 4001) with API
access, and tick **Read-Only API** in Gateway settings as an extra guard.

## Commands

### /ib-positions-overview — read-only enriched positions overview

```bash
{baseDir}/../.venv/bin/python {baseDir}/scripts/positions_overview.py --config .ib-suite/config.yaml
```

Prints one JSON object to stdout (parseable). It reads position state live and
does not write to the data lake — nothing is persisted.

## What each position carries (the 14 requested fields)

| # | Report field | JSON key | Source |
|---|---|---|---|
| 1 | Symbol | `symbol` | `contract.symbol` |
| 2 | Instrument name | `name` | `reqContractDetails().longName` |
| 3 | Asset type | `sec_type` | `contract.secType` (STK/OPT/…) |
| 4 | Quantity | `quantity` | `portfolio().position` |
| 5 | Long / short | `side` | derived: sign of quantity (LONG/SHORT/FLAT) |
| 6 | Average cost | `avg_cost` | `portfolio().averageCost` |
| 7 | Current price | `market_price` | `portfolio().marketPrice` |
| 8 | Market value | `market_value` | `portfolio().marketValue` (multiplier-correct) |
| 9 | Unrealized P&L | `unrealized_pnl` | `portfolio().unrealizedPNL` |
| 10 | Unrealized return | `unrealized_return` | derived: `pnl / |cost basis|` |
| 11 | Account weight | `weight` | derived: `base_value / NetLiquidation` |
| 12 | Industry | `industry` | `reqContractDetails().industry` |
| 13 | Market / country | `market` / `country` | `contract.primaryExchange` → country map |
| 14 | Currency | `currency` | `contract.currency` |

Value (8) and P&L (9) come straight from IB's `portfolio()`, so options are
already multiplier-correct — this skill never recomputes `qty × price`.

## Rankings and concentration (computed in the script, deterministic)

The output also carries `rankings` (symbol lists) and `top_concentration`, so
you present them verbatim without re-deriving any order:

| View | JSON key | Order |
|---|---|---|
| By market value | `rankings.by_market_value` | base `market_value`, high → low |
| By profit | `rankings.by_profit` | base `unrealized_pnl`, high → low |
| By loss | `rankings.by_loss` | base `unrealized_pnl`, most negative first |
| By account weight | `rankings.by_weight` | signed `weight`, high → low |
| Most concentrated | `top_concentration` | single position with the largest `|weight|` |

Present all four rankings, then state the `top_concentration` name and its
weight as the concentration conclusion.

## Multi-currency

Each position keeps its own quote `currency`; `fx_rate` (from IB's
`$LEDGER-ExchangeRate` ledger, local → base) yields `base_value` /
`base_unrealized_pnl`. All ranking and weighting use these base-currency values
— summing raw `market_value` across currencies would misstate the book. Rates
are taken verbatim from IB, so figures reconcile with the account and work
without a live market-data subscription.

## Notes

- `weight` and every ranking are normalized against `NetLiquidation`; `weight`
  is signed, so shorts carry a negative weight but are still surfaced by
  `top_concentration` via absolute value.
- `country` is mapped from the listing exchange; venues outside the built-in map
  (or the `SMART` router) leave `country` blank rather than guessing.
- Same `clientId` allows only one active Gateway connection — the shared
  `config.yaml` id is reused; close other sessions if the connect stalls.
- Read-only guarantee: the entry script imports no order API and connects with
  `readonly=True`. Do not add a write path here.
