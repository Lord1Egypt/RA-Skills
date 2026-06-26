---
name: kalshi-paper-trading
description: Kalshi-native paper trading ledger and CLI for binary prediction contracts. Use for paper opens, marks, reconciliation, valuation, and review without relying on the generic spot-style paper trader.
homepage: https://docs.kalshi.com
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: [node]
---

# Kalshi Paper Trading

Use this skill for Kalshi paper execution and ledger management.

Kalshi-native paper trading should use a dedicated ledger and CLI rather than the generic `paper-trading` skill.

## When to Use

Use this skill when the user wants to:

- design or build a Kalshi-specific paper trader
- inspect or reconcile Kalshi paper positions
- store Kalshi prices correctly in cents without mixing units
- compute Kalshi realized and unrealized PnL
- add Kalshi-native exposure or risk rules

## Key Rule

Do not route Kalshi paper executions through the generic `skills/paper-trading` ledger unless the user explicitly asks to keep that compatibility.

Default assumptions for this skill:

- Kalshi execution prices are stored as integer cents in `[0, 100]`
- settlement is `100` or `0` cents
- positions are keyed by `market_ticker + contract_side`
- risk controls are based on premium and event exposure, not stop-distance percent risk
- live market sync supports both legacy cent fields and modern Kalshi `*_dollars` quote fields

## Primary Commands

Initialize the paper account:

```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts init --account kalshi --starting-balance-usd 1000
```

Check status:

```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts status --account kalshi --format json --pretty
```

Sync a live market quote into the ledger:

```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts sync-market --market <TICKER> --format json --pretty
```

Open a paper trade from the live Kalshi ask:

```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts buy-from-market --account kalshi --market <TICKER> --side YES --contracts 1 --format json --pretty
```

Reconcile a finalized market:

```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts reconcile --account kalshi --market <TICKER> --winning-side YES
```

Review account performance:

```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts review --account kalshi --format json --pretty
```

## Integration

Pair this skill with a separate Kalshi API read skill for:

- market discovery
- liquidity validation
- trades and orderbook checks
- pre-trade candidate ranking

This skill owns the paper ledger and execution side only.

## Design Reference

Read the proposal before making structural changes:

- [references/kalshi-paper-ledger.md](references/kalshi-paper-ledger.md)

Use that document for:

- schema design
- command surface
- valuation rules
- settlement logic
- migration plan away from the generic paper trader

## Tests

Run the Kalshi paper-trader test file:

```bash
node --test {baseDir}/tests/kalshi_paper.test.mjs
```
