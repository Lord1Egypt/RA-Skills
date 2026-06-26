# Risk Management Rules

## Hard Rules (Never Break)

1. **Minimum edge: 4%** — Never trade below this threshold
2. **Quarter-Kelly sizing** — Full Kelly is too aggressive. Use 25% of Kelly fraction.
3. **Max 15% bankroll per position** — No single trade risks more than 15%
4. **Max 30% total exposure** — Total open positions never exceed 30% of bankroll
5. **5% max drawdown** — Stop trading if account drops 5% from peak
6. **No duplicate positions** — YES on Player A = NO on Player B. Check both sides.
7. **Min 60% confidence in your probability estimate**
8. **Document every trade BEFORE placing it** — Source data, true prob, EV, size

## Sizing Formula

```
edge = true_probability - price
odds = (1 / price) - 1
kelly = (true_prob * odds - (1 - true_prob)) / odds
size = kelly * 0.25 * bankroll
contracts = floor(size / price)
```

## When to Exit

- **Profit target:** 10-15% gain → sell
- **Stop loss:** -33% → exit
- **Trailing stop:** Lock in gains with 10% trailing floor
- **Pre-event:** Exit before event starts if edge has closed

## Common Mistakes

1. **Riding to resolution** — Take profits at 10-15%, don't be greedy
2. **Full-porting coin flips** — Only trade REAL mispricings
3. **Trusting array indices** — Always match by name, not position
4. **Stale data** — Live odds move fast. Re-check before executing.
5. **Ignoring fees** — Kalshi charges per contract. Factor into EV calc.
