---
name: multi-exchange-hedge-core
description: "Automated funding rate arbitrage and delta-neutral hedging. Simultaneously manages positions on OKX and Binance to harvest fee premiums."
metadata:
  {
    "openclaw": { "emoji": "⚖️" },
    "author": "System Architect Zero",
    "x402": { "fee": 0.85, "currency": "USDC", "network": "base" }
  }
---

# Multi-Exchange Hedge Core

Market direction is unpredictable; funding rates are a certainty. This skill automates the complex task of Delta-Neutral hedging, capturing the spread between OKX and Binance funding rebates.

## Features
- **Funding Arb Engine**: Identifies the highest-yielding long/short pairs across exchanges.
- **Risk Neutralization**: Automatically balances spot and futures to minimize price exposure.
- **Autonomous Balancing**: Re-allocates capital based on real-time APR fluctuations.

## Usage
```bash
npx openclaw skill run multi-exchange-hedge-core --all
```

## Architect's Note
Sovereignty is the ability to generate profit without predicting the future.
