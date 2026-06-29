---
name: market-tick
description: Cross-asset market tick: price, volume, and spread snapshot
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/market-tick
    emoji: "📡"
---
# market-tick

## What It Does
Cross-asset market tick: price, volume, and spread snapshot. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- For a cross-asset snapshot in a single call
- When building portfolio dashboards
- To monitor spread and volume simultaneously

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/market-tick
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/market-tick",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "btc": 67482.50,
  "eth": 3541.20,
  "sol": 152.30,
  "regime": "RANGING",
  "momentum": "BUILDING",
  "fg": 42,
  "timestamp": "2026-06-23T14:00:00Z"
}
```

## Pricing
**$0.01/call** — standard price

Early adopters automatically receive 30% off ($0.01/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [btc-price-tick](https://apexrunner.ai/signals/btc-price-tick)
- [apex-pulse](https://apexrunner.ai/signals/apex-pulse)
- [volume-analysis](https://apexrunner.ai/signals/volume-analysis)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
