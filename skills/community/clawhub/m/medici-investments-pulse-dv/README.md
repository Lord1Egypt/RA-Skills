# Market Pulse Monitor

Quick market health snapshot for active traders covering trend, volatility, breadth, and sentiment.

## Description

Market Pulse Monitor provides a rapid assessment of current market conditions by analyzing key indicators: trend strength (SPY, QQQ, IWM), volatility (VIX), breadth (advance/decline ratio), sentiment (put/call ratios), and sector rotation (leaders/laggards). Designed for morning prep, mid-day check-ins, and pre-trade environment assessment.

## Key Features

- **Trend strength** - Major indices (SPY, QQQ, IWM) direction and momentum
- **Volatility check** - VIX level, percentile, and trend
- **Breadth snapshot** - Advance/decline ratio for market participation
- **Sentiment gauge** - Put/call ratio for crowd positioning
- **Sector rotation** - Leaders (tech, healthcare) vs. laggards (energy, financials)
- **One-paragraph summary** - Synthesized market state in plain English
- **Fast execution** - Under 10 seconds for complete market snapshot

## Quick Start

```bash
# Install dependencies
pip install yfinance pandas

# Run market pulse check
python3 scripts/market_pulse.py

# Save to file
python3 scripts/market_pulse.py --output pulse_$(date +%Y%m%d).txt
```

**Output:**
```
MARKET PULSE - 2025-03-14 09:30:00 PST

Trend: SPY +0.3% (uptrend), QQQ +0.5% (strong), IWM -0.1% (weak)
Volatility: VIX 15.2 (calm, -2% from yesterday)
Breadth: 1,245 advancing / 982 declining (positive)
Sentiment: P/C ratio 0.85 (neutral)
Sector Leaders: Technology, Healthcare
Sector Laggards: Energy, Financials

Summary: Market showing healthy breadth with tech leadership. Low volatility 
environment. Small caps underperforming—concentration risk present but participation 
is positive. Neutral sentiment (no extremes). Overall: constructive for long entries.
```

## When to Use

- **Morning prep** - Before market open, assess overnight moves
- **Mid-day check** - Confirm market character hasn't shifted
- **Pre-trade** - Verify market conditions support your trade direction
- **Risk management** - Detect sudden volatility or breadth deterioration

## What It Does NOT Do

- Does NOT provide trade recommendations or stock picks
- Does NOT predict future market movements
- Does NOT track individual positions (use position-sizer for that)
- Does NOT replace detailed technical analysis
- Does NOT monitor after-hours or pre-market exclusively (uses most recent data)

## Requirements

- Python 3.8+
- yfinance library (free Yahoo Finance data)
- Internet connection
- No API keys required

## License

MIT
