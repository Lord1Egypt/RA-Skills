---
name: grid-health-score
description: Comprehensive grid health score with recommendations for optimisation
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/grid-health-score
    emoji: "🏥"
---
# grid-health-score

## What It Does
Comprehensive grid health score with recommendations for optimisation. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- For comprehensive grid performance review
- Before modifying grid parameters
- In weekly performance reporting workflows

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/grid-health-score
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/grid-health-score",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "score": 0.81,
  "grade": "A",
  "recommendations": ["Widen BTC spacing by 0.1%"]
}
```

## Pricing
**$3.00/call** — standard price

Early adopters automatically receive 30% off ($2.10/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [grid-health](https://apexrunner.ai/signals/grid-health)
- [grid-levels](https://apexrunner.ai/signals/grid-levels)
- [live-fill-rate](https://apexrunner.ai/signals/live-fill-rate)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
