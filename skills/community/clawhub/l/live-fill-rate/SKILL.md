---
name: live-fill-rate
description: Live grid fill rate across all pairs — measures execution efficiency
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/live-fill-rate
    emoji: "⚙️"
---
# live-fill-rate

## What It Does
Live grid fill rate across all pairs — measures execution efficiency. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To monitor grid execution efficiency
- To detect liquidity degradation
- When diagnosing underperforming grids

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/live-fill-rate
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/live-fill-rate",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "fill_rate_pct": 84,
  "period_hours": 24,
  "pairs": {"BTC": 91, "ETH": 79, "SOL": 82, "AVAX": 84}
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
- [grid-health](https://apexrunner.ai/signals/grid-health)
- [live-atr-sizing](https://apexrunner.ai/signals/live-atr-sizing)
- [execution-window-optimizer](https://apexrunner.ai/signals/execution-window-optimizer)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
