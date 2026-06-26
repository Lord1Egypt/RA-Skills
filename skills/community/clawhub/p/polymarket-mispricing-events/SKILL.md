---
name: polymarket-mispricing-events
description: Detects mispricings on Polymarket by cross-referencing Kalshi and Manifold consensus probability, then trades the gap using Kelly criterion sizing. Enters when estimated true probability diverges from Polymarket price by 15%+ with confirmation from at least one external platform.
metadata:
  author: "Mibayy"
  version: "1.0.0"
  displayName: "Polymarket Mispricing Events"
  difficulty: "intermediate"
  type: "automaton"
---

# Polymarket Mispricing Events

Detects and trades mispricings on Polymarket by comparing market prices against
a consensus probability estimated from Kalshi and Manifold using fuzzy title matching.

## Strategy

1. Fetches all active Polymarket binary markets (top 500 by liquidity)
2. For each market, searches Kalshi and Manifold for the same event via Jaccard title similarity
3. Computes weighted consensus probability (Kalshi 55%, Manifold 45%)
4. Enters if gap between consensus and Polymarket price exceeds threshold (default 15%)
5. Sizes position with quarter-Kelly criterion, capped between $5 and $50
6. Skips markets with flip-flop warnings, high slippage, or insufficient edge

## Edge

Cross-platform prediction market arbitrage. When two independent markets disagree by
15%+ on the same event, one of them is wrong. This skill bets on the consensus.

## When it works best

- Political, macro, and sports markets with active Kalshi/Manifold counterparts
- Events with clear resolution criteria
- Markets in the 15%-85% probability range (not near-resolved)

## Configuration (env vars)

| Variable | Default | Description |
|----------|---------|-------------|
| SIMMER_API_KEY | required | Your Simmer API key |
| TRADING_VENUE | sim | sim for paper, live for real money |
| EVENTS_ENTRY_THRESHOLD | 0.15 | Minimum gap to enter (15%) |
| EVENTS_KELLY_FRACTION | 0.25 | Kelly multiplier (0.25 = quarter-kelly) |
| EVENTS_TRADE_SIZE_MIN | 5.0 | Minimum trade size in USD |
| EVENTS_TRADE_SIZE_MAX | 50.0 | Maximum trade size in USD |
| EVENTS_MAX_POSITIONS | 8 | Maximum open positions |
| EVENTS_MIN_LIQUIDITY | 500.0 | Minimum market liquidity |
| EVENTS_MAX_GAP_CAP | 0.35 | Reject gaps > 35% (model likely wrong) |

## Risk

- Cross-platform matching via fuzzy text can produce false positives — keep position sizes conservative
- Rare markets may have no Kalshi/Manifold counterpart — these are skipped
- Kelly sizing still carries variance risk; recommend starting with sim venue
