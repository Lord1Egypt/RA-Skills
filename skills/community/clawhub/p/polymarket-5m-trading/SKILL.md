---
name: polymarket-5m-trading
description: Find a high-volume BTC-related Polymarket priced between 40% and 60%, buy 1 USD of YES, hold for 5 minutes, sell, wait 5 minutes, and repeat until 10 completed buy cycles.
metadata:
  author: "GitHub Copilot"
  version: "1.0.0"
  displayName: "Polymarket 5m Trading"
  difficulty: "intermediate"
---

# Polymarket 5m Trading

> **This is a template.** The default signal is structural rather than predictive:
> select one BTC-related market with relatively high volume and a YES price in the
> 40%-60% band, then run a fixed intraday cycle of buy, hold, sell, pause, repeat.
> Remix it by changing the BTC filter, market ranking rule, hold time, side,
> or sizing model. The skill handles market discovery, signed order creation,
> order tagging, and loop control.

## Strategy

1. Search Polymarket for BTC-related events
2. Flatten event results into tradable sub-markets
3. Keep only candidates whose YES price is between 0.40 and 0.60
4. Rank candidates by available volume fields and select the highest-volume market
5. Buy approximately 1 USD of YES using a market-style FAK order
6. Hold for 5 minutes
7. Sell the acquired YES shares using a market-style FAK order
8. Wait another 5 minutes
9. Repeat until 10 buys have completed

## Important Behavior

- The script defaults to dry-run
- Real trading requires `--live`
- Live trading requires `WALLET_PRIVATE_KEY`
- The skill uses `source` and `skillSlug` on every live order
- The skill checks market context before every buy
- The skill exits the position after the hold period even if context warnings appear
- If the selected market cannot support an approximately 1 USD entry because its minimum order size is too large, the run stops loudly

## Inputs

Required for dry-run:

- `AIONMARKET_API_KEY` or `AION_API_KEY`

Required for live trading:

- `AIONMARKET_API_KEY` or `AION_API_KEY`
- `WALLET_PRIVATE_KEY`

Optional:

- `AIONMARKET_BASE_URL`
- `BUY_USD`
- `HOLD_SECONDS`
- `MAX_BUYS`
- `SEARCH_LIMIT`
- `MARKET_PRICE_BUFFER`

## Run Examples

Preview the full plan without sending trades:

```bash
python run_skill.py
```

Run the live strategy:

```bash
python run_skill.py --live
```

Shorten the hold window for testing:

```bash
python run_skill.py --hold-seconds 10
```

## Remix Ideas

- Trade NO instead of YES
- Re-rank candidates using liquidity or recent order flow
- Re-select a fresh BTC market before each new buy cycle
- Add stop-loss or max-drawdown exits
- Replace the fixed 1 USD size with volatility-scaled sizing

