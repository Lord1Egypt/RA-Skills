---
name: momentum-status
description: Current momentum engine status across BTC, ETH, SOL, and AVAX
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/momentum-status
    emoji: "🚀"
---
# momentum-status

## What It Does
Current momentum engine status across BTC, ETH, SOL, and AVAX. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- Before momentum-based entries
- To confirm momentum engine is active
- To check multi-coin momentum alignment

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/momentum-status
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/momentum-status",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "BTC": "active",
  "ETH": "active",
  "SOL": "inactive",
  "AVAX": "inactive"
}
```

## Pricing
**$0.50/call** — standard price

Early adopters automatically receive 30% off ($0.35/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [trend-confirmed](https://apexrunner.ai/signals/trend-confirmed)
- [combined-alpha](https://apexrunner.ai/signals/combined-alpha)
- [apex-composite](https://apexrunner.ai/signals/apex-composite)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
