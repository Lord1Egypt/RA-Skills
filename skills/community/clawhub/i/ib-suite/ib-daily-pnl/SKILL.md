---
name: ib-daily-pnl
description: Read-only daily (today's) P&L breakdown from Interactive Brokers. Use when the user asks how their account did today, today's total/realized/unrealized P&L, which positions contributed the most profit or loss today, how each asset class (stock/option/ETF/forex) or currency contributed, or whether one name dominated today's move. Reads live P&L state only — never places, modifies, or cancels an order.
metadata:
  openclaw:
    requires:
      bins: [python3]
      config: [config.yaml]
    os: [darwin, linux]
---

# ib-daily-pnl

Read-only daily P&L breakdown for the IB analyst toolchain. Answers "how did my
account do today, and who moved it?" in one call: today's total P&L split into
realized and unrealized, every position's contribution ranked into winners and
losers, aggregated by asset class and by currency, with the single position that
moved today's number the most flagged. This skill connects with `readonly=True`
and only reads; it NEVER places, modifies, or cancels an order.

## Why this is a live pull (not the data lake)

Daily P&L is an IB **session** concept — it resets every trading day and exists
only on a live connection. It is NOT in the `/ib-sync` snapshot, so this skill
connects directly and reads IB's `pnl` subscription (`reqPnL` for account
totals, `reqPnLSingle` per position). Nothing is persisted. IB reports every
P&L figure already in the account base currency, so contributions sum directly
with no FX step here.

## Prerequisites

Config and the shared venv are owned by the `ib-suite` index skill (see its
first-run setup). Start IB Gateway (paper on 4002 / live on 4001) with API
access, and tick **Read-Only API** in Gateway settings as an extra guard.

## Commands

### /ib-daily-pnl — read-only daily P&L breakdown

```bash
{baseDir}/../.venv/bin/python {baseDir}/scripts/daily_pnl.py --config .ib-suite/config.yaml
```

Prints one JSON object to stdout (parseable). It reads live P&L state and does
not write to the data lake — nothing is persisted.

## What the output carries

Account totals (base currency, from `reqPnL`):

| Report field | JSON key | Source |
|---|---|---|
| Today's total P&L | `daily_pnl` | `reqPnL().dailyPnL` |
| Realized P&L (today) | `realized_pnl` | `reqPnL().realizedPnL` |
| Unrealized P&L | `unrealized_pnl` | `reqPnL().unrealizedPnL` |

Per position (`positions[]`, base currency, from `reqPnLSingle`):

| Report field | JSON key | Source |
|---|---|---|
| Symbol | `symbol` | `contract.symbol` |
| Instrument name | `name` | `reqContractDetails().longName` |
| Asset type | `sec_type` | `contract.secType` (STK/OPT/CASH/…) |
| Asset class | `asset_class` | derived: STK+stockType → Stock/ETF; OPT → Option; CASH → Forex |
| Today's P&L | `daily_pnl` | `reqPnLSingle().dailyPnL` |
| Realized P&L (today) | `realized_pnl` | `reqPnLSingle().realizedPnL` |
| Unrealized P&L | `unrealized_pnl` | `reqPnLSingle().unrealizedPnL` |
| Trading currency | `currency` | `contract.currency` |

## Rankings and attribution (computed in the script, deterministic)

Present these verbatim without re-deriving any order:

| View | JSON key | Order / content |
|---|---|---|
| Profit contribution | `rankings.by_profit_contrib` | `daily_pnl`, high → low (winners) |
| Loss contribution | `rankings.by_loss_contrib` | `daily_pnl`, most negative first (losers) |
| By asset class | `attribution.by_asset_class` | `{class: summed daily_pnl}` |
| By currency | `attribution.by_currency` | `{currency: summed daily_pnl}` |
| Top driver | `top_driver` | single position with the largest `|daily_pnl|`, plus `share_of_gross` |

List at least the top 10 by profit and the top 10 by loss (or all positions if
fewer). State the `top_driver` name, its P&L, and its `share_of_gross` as the
single-name concentration conclusion.

## What this skill will NOT fabricate (price vs vol vs theta vs FX)

A single read-only pull gives each name's **net** daily P&L, not its
decomposition into price change vs. implied-volatility change vs. time-value
decay (theta) vs. FX change. That split needs day-over-day Greeks and
exchange-rate history this snapshot does not contain. The output ships that
boundary verbatim in `attribution.note`. Report it as a data limitation and use
the asset-class buckets as the honest proxy:

- **Stock / ETF** P&L ≈ price change.
- **Forex** (CASH) P&L ≈ FX change.
- **Option** P&L blends price / volatility / theta — do not claim a precise
  split without cross-day Greeks.

For a true decomposition, capture daily Greek/FX snapshots over time (a separate,
larger change) — do not invent numbers from one pull.

## Notes

- Every P&L figure is base currency (IB converts before publishing the pnl
  subscription), so contributions sum directly; `currency` is kept only for the
  per-currency breakdown, not for conversion.
- All `pnl`/`pnlSingle` subscriptions are always cancelled after reading — this
  is a read-only pull that leaves no live subscriptions behind.
- Same `clientId` allows only one active Gateway connection — the shared
  `config.yaml` id is reused; close other sessions if the connect stalls.
- Read-only guarantee: the entry script imports no order API and connects with
  `readonly=True`. Do not add a write path here.
