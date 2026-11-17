---
name: market-tick
description: "Paid x402 endpoint: $0.014 USDC per call on Base. Returns BTC, ETH and SOL prices, market regime, Fear & Greed, and a momentum label."
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
Minimal live tick in one small JSON object: BTC, ETH and SOL prices, a one-word market regime, the Fear & Greed value, and a momentum label. Prices are Hyperliquid mid prices (with a secondary feed if Hyperliquid does not price a coin); regime is APEX's BTC regime classification; momentum is an ADX + volume label on BTC. If any input is unavailable the endpoint answers 503 and you are not charged.

## When to Use
- For a cheap, frequent BTC/ETH/SOL price check
- To read the current market regime and sentiment in one call
- As a lightweight polling input for a trading agent

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/market-tick
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
client.register_policy(max_amount(20000))  # never sign more than the list price ($0.02 USDC)

session = wrapRequestsWithPayment(requests.Session(), client)
response = session.get("https://apexrunner.ai/signals/market-tick")
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
**$0.02/call** — standard price

Every caller is charged $0.014/call until 2027-01-01 under the
early-adopter discount (30% off the standard price). No tier, no wallet
history, no enrolment — that is simply the price.

## Related Signals
- [btc-price-tick](https://apexrunner.ai/signals/btc-price-tick)
- [apex-pulse](https://apexrunner.ai/signals/apex-pulse)
- [volume-analysis](https://apexrunner.ai/signals/volume-analysis)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
