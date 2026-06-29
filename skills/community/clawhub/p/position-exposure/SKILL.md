---
name: position-exposure
description: Current position exposure by pair, strategy, and exchange
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/position-exposure
    emoji: "🎚️"
---
# position-exposure

## What It Does
Current position exposure by pair, strategy, and exchange. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- For real-time portfolio monitoring
- Before adding correlated positions
- When rebalancing across exchanges

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/position-exposure
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/position-exposure",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "total_deployed_usd": 1840,
  "by_pair": {"BTC": 620, "ETH": 480, "SOL": 420, "AVAX": 320},
  "exposure_pct": 61
}
```

## Pricing
**$2.00/call** — standard price

Early adopters automatically receive 30% off ($1.40/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [portfolio-heat](https://apexrunner.ai/signals/portfolio-heat)
- [live-atr-sizing](https://apexrunner.ai/signals/live-atr-sizing)
- [agent-stress-index](https://apexrunner.ai/signals/agent-stress-index)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
