---
name: market-pulse-bundle
description: "Paid x402 endpoint: $0.007 USDC per call on Base. Returns price tick + Fear & Greed + regime in one call."
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/market-pulse-bundle
    emoji: "📦"
---
# market-pulse-bundle

## What It Does
Bundle: price tick + Fear & Greed + regime in one call. Computed by APEX Runner from live market data, not from backtests.

## When to Use
- When a quick market snapshot is needed
- At the start of an agent decision loop
- To reduce latency with a single bundled call

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/market-pulse-bundle
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
response = session.get("https://apexrunner.ai/signals/market-pulse-bundle")
print(response.json())
```

## Example Response
```json
{
  "btc_price_tick": {"b": 67482.50, "e": 3541.20, "s": 152.30, "a": 24.10, "t": 1750000000},
  "fear_greed": {"value": 42, "classification": "Fear", "zone": "FEAR", "source": "cmc"},
  "regime": {"regime": "RANGING", "confidence": 0.82, "coin": "BTC"},
  "timestamp": "2026-06-23T14:00:00Z"
  // Full nested output of all component signals returned in one call
}
```

## Pricing
**$0.01/call** — standard price

Every caller is charged $0.007/call until 2027-01-01 under the
early-adopter discount (30% off the standard price). No tier, no wallet
history, no enrolment — that is simply the price.

## Related Signals
- [trading-intelligence-bundle](https://apexrunner.ai/signals/trading-intelligence-bundle)
- [regime](https://apexrunner.ai/signals/regime)
- [fear-greed](https://apexrunner.ai/signals/fear-greed)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
