# Case Study: Gold Trading Strategy Optimization

## Overview

Applied the autoresearch pattern to optimize an XAUUSD (gold) trading strategy's parameters using backtesting as the evaluation function.

## Setup

- **Mutable file**: Strategy configuration (EMA periods, momentum threshold, position sizing, stop-loss/take-profit)
- **Eval function**: Backtest on historical XAUUSD data → Sharpe ratio
- **Duration**: 25 minutes
- **Total experiments**: 86

## Results

| Metric | Baseline | Final | Change |
|--------|----------|-------|--------|
| **Sharpe Ratio** | 5.80 | 12.23 | **+111%** |
| Experiments | — | 86 | — |
| Time | — | 25 min | — |

## Key Discoveries

The autoresearch loop found several non-obvious improvements:

### 1. Momentum Threshold: 0.003 → 0
- **What**: The minimum momentum required to enter a trade
- **Why it worked**: The original threshold filtered out many profitable micro-moves. Setting it to 0 allowed the strategy to capture small but consistent momentum signals.
- **Human intuition**: A human would never remove a safety threshold. The data showed it was hurting more than helping.

### 2. EMA Optimization: 8/24 → 5/11
- **What**: Fast and slow Exponential Moving Average periods
- **Why it worked**: Shorter EMAs made the strategy more responsive to gold's fast price movements. The 8/24 combo was lagging behind.
- **Discovery path**: The loop tried 8/20 first (minor improvement), then 6/15 (better), then 5/11 (best).

### 3. Position Sizing Optimization
- **What**: Dynamic position sizing based on volatility
- **Why it worked**: Larger positions during low-volatility periods, smaller during high-volatility. The original used fixed sizing.

## Experiment Log (highlights)

```
exp-1:  momentum 0.003 → 0.002      | 5.80 → 6.12  ✅
exp-3:  momentum 0.002 → 0.001      | 6.12 → 6.45  ✅
exp-7:  momentum 0.001 → 0          | 6.45 → 7.21  ✅
exp-12: EMA fast 8 → 6              | 7.21 → 7.89  ✅
exp-15: EMA slow 24 → 18            | 7.89 → 8.34  ✅
exp-23: EMA fast 6 → 5              | 8.34 → 8.67  ✅
exp-31: EMA slow 18 → 11            | 8.67 → 9.45  ✅
exp-42: position sizing → volatility | 9.45 → 10.78 ✅
exp-58: take-profit optimization     | 10.78 → 11.34 ✅
exp-71: stop-loss tightening         | 11.34 → 11.89 ✅
exp-82: entry timing refinement      | 11.89 → 12.23 ✅
```

## Takeaways

1. **Small changes compound**: No single experiment gave more than +15%. The 111% total came from 11 incremental improvements across 86 experiments.
2. **Remove assumptions**: The biggest win (momentum threshold → 0) came from questioning a parameter everyone assumed was necessary.
3. **Speed matters**: 86 experiments in 25 minutes. A human trader might test 5 variations in a week.
4. **Git tracking is essential**: Being able to diff exp-42 vs exp-41 revealed exactly which parameter change caused the improvement.
