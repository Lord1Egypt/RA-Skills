---
name: narrative-intelligence
description: "Paid x402 endpoint: $0.007 USDC per call on Base. Returns AI-synthesised market narrative with directional bias score."
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

> **Tier 3 — Strategic Edge**: A composite signal that combines several of APEX Runner's market models into one higher-level reading.

## What It Does
AI-synthesised market narrative with directional bias score. Computed by APEX Runner from live market data, not from backtests.

## When to Use
- To understand AI agent market consensus
- For macro context before directional bets
- When narrative momentum matters

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/narrative-intelligence
```

The x402 client handles payment automatically. No API key, no account, no subscription — just an EVM wallet with USDC on Base mainnet (no ETH needed).

```python
# pip install "x402[evm,requests]"
import os

import requests
from eth_account import Account
from x402 import max_amount, x402ClientSync
from x402.http.clients import wrapRequestsWithPayment
from x402.mechanisms.evm.exact import register_exact_evm_client
from x402.mechanisms.evm.signers import EthAccountSigner

client = x402ClientSync()
register_exact_evm_client(client, EthAccountSigner(Account.from_key(os.environ["EVM_PRIVATE_KEY"])))
client.register_policy(max_amount(10000))  # never sign more than the list price ($0.01 USDC)

session = wrapRequestsWithPayment(requests.Session(), client)
response = session.get("https://apexrunner.ai/signals/narrative-intelligence")
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
**$0.01/call** — standard price

Every caller is charged $0.007/call until 2027-01-01 under the
early-adopter discount (30% off the standard price). No tier, no wallet
history, no enrolment — that is simply the price.

## Related Signals
- [whale-sentiment](https://apexrunner.ai/signals/whale-sentiment)
- [regime](https://apexrunner.ai/signals/regime)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
