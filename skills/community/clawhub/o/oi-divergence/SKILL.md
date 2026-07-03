---
name: oi-divergence
description: Open interest divergence from price — detects smart-money positioning
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/oi-divergence
    emoji: "📊"
---
# oi-divergence

## What It Does
Open interest divergence from price — detects smart-money positioning. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To detect divergence between OI and price
- Before directional trades
- To identify smart money vs retail positioning

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/oi-divergence
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/oi-divergence",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "divergence": true,
  "oi_trend": "rising",
  "price_trend": "falling",
  "signal": "bearish"
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
- [whale-sentiment](https://apexrunner.ai/signals/whale-sentiment)
- [liquidation-pressure](https://apexrunner.ai/signals/liquidation-pressure)
- [funding-rate](https://apexrunner.ai/signals/funding-rate)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
