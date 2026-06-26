# Self-Improvement Algorithm Reference

## Overview

The agent evaluates its own performance every N loops and adjusts strategy parameters
in `memory/strategies.json`. Each adjustment is versioned. No parameter change is applied
to live execution without first being validated in `suggest_improvements()`.

## Evaluation Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Win Rate | wins / total_trades | > 50% |
| Profit Factor | sum(wins) / abs(sum(losses)) | > 1.5 |
| Sharpe Ratio | mean(pnl) / std(pnl) * √252 | > 1.0 |
| Max Drawdown | max(peak - cumulative) | < 5% of account |
| Avg Holding Time | mean(holding_minutes) | Strategy-dependent |

## Improvement Rules

### RSI Mean Reversion
- **Win rate < 45%**: Tighten oversold/overbought thresholds by ±5
  - Oversold: 30 → 25 (harder to trigger, cleaner signals)
  - Overbought: 70 → 75
- **Win rate > 60% for 20+ trades**: Loosen thresholds slightly for more signals

### MACD Momentum
- **Profit factor < 1.2**: Raise `min_histogram` by 25% (filter weak crossovers)
- **Too few signals (< 1/day avg)**: Lower `min_histogram` by 10%

### Universal (all strategies)
- If max drawdown > 4%: Reduce `atr_stop_multiplier` from 2.0 → 1.5
- If avg holding time < 30min and Sharpe < 0.5: Suspect noise — raise signal confidence threshold

## Versioning

Every parameter change creates a new version entry in `memory/strategies.json`:

```json
{
  "version": 3,
  "timestamp": "2025-06-01T12:00:00+00:00",
  "source": "self_improvement",
  "params": { ... },
  "recommendations": [
    {
      "strategy": "rsi_mean_reversion",
      "param": "oversold",
      "old": 30,
      "new": 25,
      "reason": "Win rate 42% — tightening RSI thresholds"
    }
  ]
}
```

## Safety Constraints on Self-Improvement

- Parameters never change by more than 20% in one step
- `rsi_mean_reversion.oversold` never goes below 15 or above 35
- `rsi_mean_reversion.overbought` never goes below 65 or above 85
- `max_risk_per_trade_pct` is NOT auto-tuned (human-controlled only)
- Changes are logged but human can revert via setting `current_version` back

## Reverting to a Previous Version

```python
import json

with open("memory/strategies.json") as f:
    data = json.load(f)

# Roll back to version 2
target_version = 2
for v in data["versions"]:
    if v["version"] == target_version:
        data["current_version"] = target_version
        # Manually update config/settings.yaml params from v["params"]
        break

with open("memory/strategies.json", "w") as f:
    json.dump(data, f, indent=2)
```

## Extending the Improvement Loop

To add a new tunable parameter:
1. Add a rule in `performance.py → suggest_improvements()`
2. Apply it in `apply_improvements()` via `strategy_engine.update_params()`
3. Document the rule and its bounds here
4. Add a safety constraint check
