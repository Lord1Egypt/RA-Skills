# Confluence Model

## Checks (9-point system, implemented in `scripts/compute_confluence.py`)

| # | Check | Description |
|---|---|---|
| 1 | `trend_alignment` | 1H trend agrees with trade direction; 4H trend at least neutral |
| 2 | `momentum_confirmation` | 1H RSI-based momentum confirms direction |
| 3 | `volume_confirmation` | Current volume ≥ 75% of 20-bar average |
| 4 | `rsi_zone` | RSI in valid entry zone (long: 40–70, short: 30–60) |
| 5 | `macd_alignment` | MACD line above/below signal line in trade direction |
| 6 | `reward_risk_ok` | Reward ≥ configured `min_reward_risk` × risk (default 1.5×) |
| 7 | `exposure_capacity_ok` | Current total exposure < 90% of `max_total_exposure` |
| 8 | `position_capacity_ok` | Open positions < `max_concurrent_positions` |
| 9 | `timeframe_confluence` | Both 1H and 4H trend align with trade direction |

## Thresholds

- **New entry (long/short)**: require confidence ≥ 0.55 (5/9 checks passing)
- **High volatility override**: require confidence ≥ 0.70 to enter when `high_volatility=true`
- **Hold**: no minimum (position management runs regardless of score)
- **Close**: triggered by trend reversal or extreme RSI, not by confluence score

## Confidence → leverage mapping

| Confidence | Leverage |
|---|---|
| < 0.60 | `min_leverage` |
| 0.60 – 0.79 | midpoint of `min_leverage` – `max_leverage` |
| ≥ 0.80 | `max_leverage` |
| Any, `high_volatility=true` | Step down by 1 from above |

## Learning adjustments

After each review cycle (`update_metrics.py`):
- A `confidence_multiplier` is tracked in `state.json`
- After 4+ consecutive losses: multiplier drops (harder to reach threshold → fewer entries)
- After winning streak (win rate ≥ 55%, no recent losses): multiplier recovers toward 1.0
- The multiplier never raises leverage above the configured `max_leverage`
