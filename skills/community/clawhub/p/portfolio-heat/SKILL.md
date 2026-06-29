---
name: portfolio-heat
description: Current portfolio heat level: normal, elevated, or emergency
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/portfolio-heat
    emoji: "🌡️"
---
# portfolio-heat

## What It Does
Current portfolio heat level: normal, elevated, or emergency. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- Before adding new positions
- To enforce portfolio risk limits
- When evaluating whether to reduce exposure

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/portfolio-heat
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/portfolio-heat",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "heat_level": "elevated",
  "heat_score": 0.61,
  "action": "pause new entries"
}
```

## Pricing
**$1.00/call** — standard price

Early adopters automatically receive 30% off ($0.70/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [position-exposure](https://apexrunner.ai/signals/position-exposure)
- [agent-stress-index](https://apexrunner.ai/signals/agent-stress-index)
- [risk-assessment-bundle](https://apexrunner.ai/signals/risk-assessment-bundle)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
