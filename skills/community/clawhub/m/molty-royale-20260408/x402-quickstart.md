# Quick Start — x402 Token Purchase API

End-to-end guide to call the x402 API: check prices, pay with USDC, and receive distribution tokens. Use **Testnet** first.

---

## Prerequisites

- An **Ethereum-compatible private key** (hex, with or without `0x`).
- **USDC on Base Sepolia** (testnet). Get testnet USDC from a faucet; the payer address must hold enough USDC for the purchase.
- No prior USDC `approve()` is needed — the API uses EIP-3009 `transferWithAuthorization`.

**Base URLs:**

| Environment | Base URL |
|---|---|
| Testnet | `https://x402.crosstoken.io` |
| Production | `https://x402.crosstoken.io` |

---

## Step 1: Install SDK

### TypeScript / Node

```bash
npm install @x402/fetch @x402/evm viem
```

### Python

```bash
pip install "x402[httpx]" eth_account
```

### Go

```bash
go get github.com/coinbase/x402/go
```

---

## Step 2: Check Price

**"How much USDC for N tokens?"**

```bash
curl -s "https://x402.crosstoken.io/rates?distribution_amount=1000000000000000000" | jq .
```

**"How many tokens for N USDC?"**

```bash
curl -s "https://x402.crosstoken.io/rates?payment_amount=1500000" | jq .
```

---

## Step 3: Purchase Tokens

### TypeScript (fetch)

```ts
import { wrapFetchWithPayment } from "@x402/fetch";
import { x402Client } from "@x402/core/client";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

const BASE_URL = "https://x402.crosstoken.io";
const signer = privateKeyToAccount(process.env.EVM_PRIVATE_KEY! as `0x${string}`);
const client = new x402Client();
client.register("eip155:*", new ExactEvmScheme(signer));
const fetchWithPayment = wrapFetchWithPayment(fetch, client);

const res = await fetchWithPayment(`${BASE_URL}/purchase`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    distribution_amount: "1000000000000000000",
    recipient: "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  }),
});

if (res.status !== 202) {
  const err = await res.json();
  throw new Error(JSON.stringify(err));
}
const order = await res.json();
console.log("Order accepted:", order.order_id);
```

### Python (async httpx)

```python
import asyncio
import os
from eth_account import Account
from x402 import x402Client
from x402.http.clients import x402HttpxClient
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client

BASE_URL = "https://x402.crosstoken.io"

async def main():
    account = Account.from_key(os.environ["EVM_PRIVATE_KEY"])
    client = x402Client()
    register_exact_evm_client(client, EthAccountSigner(account))

    async with x402HttpxClient(client) as http:
        r = await http.post(
            f"{BASE_URL}/purchase",
            json={
                "distribution_amount": "1000000000000000000",
                "recipient": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            },
        )
        if r.status_code != 202:
            raise RuntimeError(r.text)
        order = r.json()
        print("Order accepted:", order["order_id"])

asyncio.run(main())
```

---

## Step 4: Track Order

```bash
curl -s "https://x402.crosstoken.io/orders/YOUR_ORDER_ID" | jq .
```

Typical flow: `payment_verified` → `distribution_completed` (or `distribution_failed`).

---

## Switching to Production

1. Change the base URL to `https://x402.crosstoken.io`.
2. Use **USDC on Base mainnet** (chain ID 8453).

No code changes besides the base URL and ensuring the wallet has mainnet USDC.

---

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| **402 then failure** | Ensure the private key matches a wallet that holds enough USDC on the correct network. |
| **429 Rate limited** | Reduce request rate; wait and retry. |
| **400 / 422** | Validate `distribution_amount` (wei string), `recipient` (valid 0x address). |
| **503** | Server or pricing temporarily unavailable; retry later. |

For full API reference and error codes, see [x402-skill.md](x402-skill.md).
