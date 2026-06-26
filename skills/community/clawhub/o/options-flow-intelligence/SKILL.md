---
name: options-flow-intelligence
description: |
  Real-time institutional options flow intelligence and momentum analysis for AI agents.
  Fetches live option flow data from OptionWhales API including current institutional flow,
  per-ticker momentum, abnormal trade detection, and direction bias indicators across major
  US equities. Built for volatility traders and algo systems decoding dark pool options activity.

  Commands:
  - optionflow.py flow           Get current market-wide option flow
  - optionflow.py momentum      View top momentum stock rankings
  - optionflow.py abnormal       Detect unusual options activity
  - optionflow.py ticker SYMBOL  Get specific ticker flow (e.g., AAPL, TSLA)

  Environment: OPTIONWHALES_API_KEY required. Python 3.7+, zero deps beyond stdlib.

  Example output includes intent_momentum scores, premium volumes, direction bias,
  and momentum rankings. Scores range from 0-100 with higher values indicating
  stronger institutional conviction. Useful for catching early signals before
  earnings events, identifying sector rotation through options flow, and building
  automated alerts for whale-sized option positions.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
allowed-tools: Bash, Read
---

# Options Flow Intelligence

Fetches real-time institutional options flow data from the OptionWhales API to detect whale trades, momentum shifts, and abnormal activity across US equities.

## Setup

Set your API key:
```bash
export OPTIONWHALES_API_KEY="your_key_here"
```

## Commands

```bash
# Market-wide flow (top 20 by momentum)
python scripts/optionflow.py flow

# Top momentum stocks
python scripts/optionflow.py momentum

# Abnormal trades (potential insider activity)
python scripts/optionflow.py abnormal

# Specific ticker deep dive
python scripts/optionflow.py ticker AAPL
python scripts/optionflow.py ticker TSLA
python scripts/optionflow.py ticker NVDA
```

## Output Interpretation

- **Signal scores** range from 0-100, higher = stronger institutional conviction
- **Direction** shows whether smart money is buying calls (bullish) or puts (bearish)
- **Premium** shows total dollar value of options activity
- **Momentum rankings** show which stocks have the strongest options activity today

## Integration with Trading Systems

The JSON output can be piped to other tools:
```bash
python scripts/optionflow.py flow | grep "BULLISH" | head -5
```

Use in automated alerting by setting up cron jobs or integrating with notification systems.

## Data Freshness

Data refreshes every few minutes. For real-time streaming, consider the WebSocket API
which is available on OptionWhales Pro plans. The current script focuses on REST API
polling which is suitable for most use cases without requiring WebSocket infrastructure.