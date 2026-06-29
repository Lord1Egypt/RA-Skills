---
name: narrative-intelligence
description: AI-synthesised market narrative with directional bias score
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/narrative-intelligence
    emoji: "📰"
---
# narrative-intelligence

> **Tier 3 — Strategic Edge**: This signal provides proprietary institutional-grade intelligence computed from APEX's live trading system. Pricing reflects the depth of analysis and the scarcity of the underlying edge.

## What It Does
AI-synthesised market narrative with directional bias score. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To understand AI agent market consensus
- For macro context before directional bets
- When narrative momentum matters

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/narrative-intelligence
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/narrative-intelligence",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "primary_narrative": "Institutional accumulation amid retail fear",
  "narrative_sentiment": "BULLISH",
  "narrative_age_days": 7,
  "saturation_level": "DEVELOPING",
  "alpha_window": "OPEN",
  "confidence": "MEDIUM",
  "timestamp": "2026-06-23T14:00:00Z"
}
```

## Pricing
**$10.00/call** — standard price

Early adopters automatically receive 30% off ($7.00/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [ai-narrative](https://apexrunner.ai/signals/ai-narrative)
- [whale-sentiment](https://apexrunner.ai/signals/whale-sentiment)
- [regime](https://apexrunner.ai/signals/regime)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
