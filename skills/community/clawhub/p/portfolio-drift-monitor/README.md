# Portfolio Drift Monitor

Real-time Kalshi portfolio drift alerts — monitors positions and fires when any moves beyond your configured threshold.

## Install

```bash
clawhub install portfolio-drift-monitor
```

## Quick Start

1. Get a Kalshi API key at https://kalshi.com (Settings → API)
2. Set environment variables: `KALSHI_KEY_ID` and `KALSHI_KEY_PATH`
3. Run: `python scripts/portfolio_drift.py`
4. Schedule hourly for continuous monitoring

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `PORTFOLIO_DRIFT_THRESHOLD` | `5.0` | Percentage change to trigger alert |
| `PORTFOLIO_DRIFT_INTERVAL` | `60` | Minutes between checks |

## Full Documentation

See [SKILL.md](SKILL.md) for complete documentation including threshold tuning profiles, ecosystem integration, and debugging.

## Part of the OpenClaw Prediction Market Trading Stack

```bash
clawhub install kalshalyst kalshi-command-center polymarket-command-center prediction-market-arbiter xpulse portfolio-drift-monitor market-morning-brief personality-engine
```

**Author**: KingMadeLLC
