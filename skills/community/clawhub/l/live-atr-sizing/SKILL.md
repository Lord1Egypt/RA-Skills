---
name: live-atr-sizing
description: Live ATR-based position sizing recommendation for current volatility
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/live-atr-sizing
    emoji: "📐"
---
# live-atr-sizing

## What It Does
Live ATR-based position sizing recommendation for current volatility. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To size positions with live volatility data
- Before every new position entry
- To enforce consistent risk-per-trade

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/live-atr-sizing
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/live-atr-sizing",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "BTC": {"atr_usd": 1240, "recommended_size_usd": 67},
  "ETH": {"atr_usd": 88, "recommended_size_usd": 42}
}
```

## Pricing
**$1.50/call** — standard price

Early adopters automatically receive 30% off ($1.05/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [live-fill-rate](https://apexrunner.ai/signals/live-fill-rate)
- [position-exposure](https://apexrunner.ai/signals/position-exposure)
- [slippage-forecast](https://apexrunner.ai/signals/slippage-forecast)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
