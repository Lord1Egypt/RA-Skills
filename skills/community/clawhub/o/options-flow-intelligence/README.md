# Options Flow Intelligence Skill

Real-time institutional options flow intelligence that fetches live data from OptionWhales API to detect whale trades, momentum shifts, and abnormal options activity across major US equities.

## Features

- **Current Option Flow** - Market-wide view of institutional option activity
- **Ticker Analysis** - Deep dive into specific stock option flow
- **Momentum Rankings** - Top stocks by options momentum score
- **Abnormal Trade Detection** - Flags unusual options activity
- **Python 3.7+ Compatible** - Zero external dependencies

## Setup

```bash
# Set your OptionWhales API key
export OPTIONWHALES_API_KEY="your_api_key_here"

# Run the script
python scripts/optionflow.py flow
python scripts/optionflow.py momentum
python scripts/optionflow.py ticker AAPL
python scripts/optionflow.py abnormal
```

## Use Cases

- Filter high-signal unusual options activity (uOA)
- Build option flow trading dashboards
- Generate automated alerts for momentum shifts
- Backtest option flow signals against price action
- Incorporate into quantitative trading models