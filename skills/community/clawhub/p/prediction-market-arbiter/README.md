# Prediction Market Arbiter

Cross-platform divergence scanner — compares Kalshi and Polymarket prices on identical events to find arbitrage opportunities.

## Install

```bash
clawhub install prediction-market-arbiter
```

## Quick Start

1. Get a Kalshi API key at https://kalshi.com (Settings → API)
2. Configure credentials in `~/.openclaw/config.yaml`
3. Run: `python scripts/arbiter.py`

Polymarket requires no API key (public Gamma API).

## How It Works

| Phase | What It Does |
|-------|-------------|
| **Fetch** | Kalshi (top 1000 markets) + Polymarket (top 200 by volume) |
| **Match** | Fuzzy title matching via Jaccard similarity |
| **Filter** | Volume threshold + divergence threshold |
| **Alert** | Sort by spread size, cache results, alert on top matches |

## Cost

$0. Both APIs are free.

## Full Documentation

See [SKILL.md](SKILL.md) for complete documentation including fuzzy matching examples, threshold tuning profiles, configuration, and divergence interpretation patterns.

## Part of the OpenClaw Prediction Market Trading Stack

```bash
clawhub install kalshalyst kalshi-command-center polymarket-command-center prediction-market-arbiter xpulse portfolio-drift-monitor market-morning-brief personality-engine
```

**Author**: KingMadeLLC
