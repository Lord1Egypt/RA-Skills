---
name: ib-options-overview
description: Read-only Interactive Brokers option positions and Greeks overview. Use when the user asks for open option contracts, IV, Delta, Gamma, Theta, Vega, moneyness, expiry exposure, or option concentration. Reads live positions only - never places, modifies, or cancels an order.
metadata:
  openclaw:
    requires:
      bins: [python3]
      config: [config.yaml]
    os: [darwin, linux]
---

# ib-options-overview

Read every open option position and return one JSON risk overview. This connects
with `readonly=True` and never places, modifies, or cancels orders.

By default it runs in **free mode** (`options.fetch_market_data: false`): it reads
only IB-computed portfolio fields (position, price, market value, unrealized P&L)
and requests no market data, so it never risks IBKR snapshot charges. Greeks, IV,
underlying price, and moneyness are unavailable in this mode.

To collect Greeks/IV, set `options.fetch_market_data: true` in `config.yaml`. The
skill then briefly subscribes for model Greeks, requests one deduplicated
underlying quote when option model data lacks an underlying price, and cancels
both subscriptions afterward. This may incur IBKR snapshot charges for symbols
without a real-time market-data subscription.

```bash
{baseDir}/../.venv/bin/python {baseDir}/scripts/options_overview.py --config .ib-suite/config.yaml
```

The JSON lists each contract's underlying, Call/Put, long/short side, strike,
expiry, inclusive calendar DTE, quantity, cost, price, market value, unrealized
P&L, IV, Delta, Gamma, Theta, Vega, and ITM/ATM/OTM state. `summary` includes
aggregate Greeks, daily time-value decay, expiry distribution, and absolute
market-value underlying concentration.

Present the result in the language of the user's current request. Start with a position-detail Markdown table,
then a moneyness Markdown table, and only then the account overview, principal risk observations, and data limitations.

The position-detail table must contain these columns in order:
`underlying_symbol`, `right`, `expiry_date`, `days_to_expiry`, `strike`,
`quantity`, `market_value`, and `unrealized_pnl`. Localize the table title,
headings, Call/Put labels, and surrounding prose; keep ticker symbols, dates,
DTE values, currency values, and ITM/ATM/OTM/UNKNOWN unchanged. Sort rows by
`expiry_date`, then `underlying_symbol`, then `strike`, all ascending. Render
strikes compactly without unnecessary trailing zeros. Render market value and
unrealized P&L to two decimal places with an explicit plus sign for positive values.
Bold the `unrealized_pnl` cells for the two largest available losses (the two most negative values);
if fewer than two losses exist, bold only those, and never bold zero or profitable values.

In the second table, group positions by `moneyness` in this order: ITM, ATM, OTM, and UNKNOWN,
including empty groups. Within each group, sort by
`underlying_symbol`, then `expiry_date`, then `strike`. For a classified
position with an underlying price, show the underlying price and the in/out-of-
the-money distance as the absolute difference between `underlying_price` and `strike`.
You may combine strikes only when symbol, right, expiry, and moneyness are
identical. Put positions with null moneyness in UNKNOWN and explain their
matching `data_limitations` after the tables.

Delayed data is accepted. Unavailable price, underlying price, IV, or Greek
fields remain `null` and are explained in `data_limitations`; no unavailable
market data is fabricated as zero.
