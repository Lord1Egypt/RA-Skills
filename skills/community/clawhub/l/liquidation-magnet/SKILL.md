---
name: liquidation-magnet
description: Identifies price levels with dense liquidation clusters
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/liquidation-magnet
    emoji: "🧲"
---
# liquidation-magnet

## What It Does
Identifies price levels with dense liquidation clusters. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To identify high-risk price zones
- Before setting stop losses
- When sizing positions near dense liquidation clusters

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/liquidation-magnet
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/liquidation-magnet",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "magnet_levels": [67000, 65500],
  "risk": "moderate",
  "distance_pct": 2.2
}
```

## Pricing
**$0.75/call** — standard price

Early adopters automatically receive 30% off ($0.52/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [liquidation-pressure](https://apexrunner.ai/signals/liquidation-pressure)
- [crowded-trade-detector](https://apexrunner.ai/signals/crowded-trade-detector)
- [oi-divergence](https://apexrunner.ai/signals/oi-divergence)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
