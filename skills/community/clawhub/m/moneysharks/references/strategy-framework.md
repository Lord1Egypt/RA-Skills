# Strategy Framework

## Principles
- Prefer 4H trend alignment.
- Use 1M for timing.
- Use 5M/15M for setup structure.
- Use 1H/4H for context.
- Require confluence before new entries.
- Prefer no trade over low-quality trades.

## Inputs
- price
- trend state
- RSI/MACD or equivalent
- EMA20 or equivalent
- support/resistance
- ATR
- volume vs average
- open interest
- funding rate
- BTC context / sentiment when available

## Outputs
- `long`
- `short`
- `wait`
- `hold`
- `close`
