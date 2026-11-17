---
name: ib-account-overview
description: Read-only account financial overview from Interactive Brokers. Use when the user asks for net liquidation, cash balance, buying power, margin (initial/maintenance/used), excess liquidity, or daily/unrealized/realized P&L, with per-currency balances converted to the base currency. Reads account state only — never positions detail, never orders.
metadata:
  openclaw:
    requires:
      bins: [python3]
      config: [config.yaml]
    os: [darwin, linux]
---

# ib-account-overview

Read-only account financial overview for the IB analyst toolchain. Answers
"how is my account doing right now?" in one call: equity, cash, buying power,
margin, liquidity, and P&L, plus a per-currency breakdown converted to the
account base currency. This skill connects with `readonly=True` and only reads;
it NEVER places, modifies, or cancels an order.

## Prerequisites

Config and the shared venv are owned by the `ib-suite` index skill (see its
first-run setup). Start IB Gateway (paper on 4002 / live on 4001) with API
access, and tick **Read-Only API** in Gateway settings as an extra guard.

## Commands

### /ib-account-overview — read-only account financial overview

```bash
{baseDir}/../.venv/bin/python {baseDir}/scripts/account_overview.py --config .ib-suite/config.yaml
```

Prints a JSON object to stdout (parseable) with the fields below. It reads
account state live and does not write to the data lake — nothing is persisted.

## Field mapping (IB tag -> report field)

| Report field | Source |
|---|---|
| Net Liquidation | `NetLiquidation` |
| Cash Balance | `TotalCashValue` |
| Buying Power | `BuyingPower` |
| Margin Used (current) | `MaintMarginReq` |
| Initial Margin Req | `FullInitMarginReq` |
| Maintenance Margin Req | `FullMaintMarginReq` |
| Available Funds | `AvailableFunds` |
| Excess Liquidity | `ExcessLiquidity` |
| Gross Position Value | `GrossPositionValue` |
| Daily P&L | `reqPnL().dailyPnL` |
| Unrealized P&L | `reqPnL().unrealizedPnL` |
| Realized P&L | `reqPnL().realizedPnL` |

Daily/unrealized/realized P&L come from IB's `pnl` subscription (not
`accountValues`); the subscription is always cancelled after reading.

## Multi-currency

Per-currency rows come from IB's `$LEDGER-*` ledger: `$LEDGER-CashBalance`,
`$LEDGER-NetLiquidationByCurrency`, and `$LEDGER-ExchangeRate` (local -> base).
Each `currency_balances` entry carries `base_cash_balance` /
`base_net_liquidation` (converted via that row's rate). The base-currency total
must use these `base_*` values — summing raw amounts mixes currencies. The
exchange rate is taken verbatim from IB's ledger, so figures reconcile with the
account and work without a live market-data subscription.

## Notes

- All monetary figures are reported in the account base currency; `Currency` from
  the account summary sets it (config `data.base_currency` overrides only when
  the account BASE is absent).
- Same `clientId` allows only one active Gateway connection — the shared
  `config.yaml` id is reused; close other sessions if the connect stalls.
- Read-only guarantee: the entry script imports no order API and connects with
  `readonly=True`. Do not add a write path here.
