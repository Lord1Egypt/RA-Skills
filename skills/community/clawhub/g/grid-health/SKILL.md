---
name: grid-health
description: "Paid x402 endpoint: $0.007 USDC per call on Base. Returns grid bot health: fill rate, inventory, and level status across pairs."
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/grid-health
    emoji: "🔲"
---
# grid-health

## What It Does
Grid bot health: fill rate, inventory, and level status across pairs. Computed by APEX Runner from live market data, not from backtests.

## When to Use
- To monitor grid bot performance
- Before adjusting grid parameters
- When diagnosing poor fill rates

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/grid-health
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
response = session.get("https://apexrunner.ai/signals/grid-health")
print(response.json())
```

## Example Response
```json
{
  "fill_rate_pct": 84,
  "inventory_pct": 61,
  "active_pairs": 4,
  "status": "healthy"
}
```

## Pricing
**$0.01/call** — standard price

Every caller is charged $0.007/call until 2027-01-01 under the
early-adopter discount (30% off the standard price). No tier, no wallet
history, no enrolment — that is simply the price.

## Related Signals
- [grid-health-score](https://apexrunner.ai/signals/grid-health-score)
- [grid-levels](https://apexrunner.ai/signals/grid-levels)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
