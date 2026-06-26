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

Pick one language. The x402 client will handle 402 Payment Required (read `PAYMENT-REQUIRED`, sign, then retry with `PAYMENT-SIGNATURE`) for you. This API uses x402 V2 headers.

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

**“How much USDC for N tokens?”**

```bash
curl -s "https://x402.crosstoken.io/rates?distribution_amount=1000000000000000000" | jq .
```

**“How many tokens for N USDC?”**

```bash
curl -s "https://x402.crosstoken.io/rates?payment_amount=1500000" | jq .
```

Amounts are in **wei strings** (e.g. `1000000000000000000` = 1 token at 18 decimals; `1000000` = 1 USDC at 6 decimals). See [x402-skill.md](x402-skill.md) for the full response shape.

---

## Step 3: Purchase Tokens

Use the same base URL and body shape; the SDK adds the `PAYMENT-SIGNATURE` header automatically after receiving 402 (with payment details in `PAYMENT-REQUIRED`).

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

### Go

```go
package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"

	x402 "github.com/coinbase/x402/go"
	x402http "github.com/coinbase/x402/go/http"
	evmclient "github.com/coinbase/x402/go/mechanisms/evm/exact/client"
	evmsigner "github.com/coinbase/x402/go/signers/evm"
)

const baseURL = "https://x402.crosstoken.io"

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 60*time.Second)
	defer cancel()

	signer, err := evmsigner.NewClientSignerFromPrivateKey(os.Getenv("EVM_PRIVATE_KEY"))
	if err != nil {
		panic(err)
	}
	client := x402.Newx402Client().Register("eip155:*", evmclient.NewExactEvmScheme(signer))
	httpClient := x402http.Newx402HTTPClient(client)

	body, _ := json.Marshal(map[string]string{
		"distribution_amount": "1000000000000000000",
		"recipient":           "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
	})
	req, _ := http.NewRequestWithContext(ctx, http.MethodPost, baseURL+"/purchase", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	req.GetBody = func() (io.ReadCloser, error) { return io.NopCloser(bytes.NewReader(body)), nil }

	resp, err := httpClient.DoWithPayment(ctx, req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != 202 {
		b, _ := io.ReadAll(resp.Body)
		panic(fmt.Sprintf("status %d: %s", resp.StatusCode, string(b)))
	}
	var order map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&order)
	fmt.Println("Order accepted:", order["order_id"])
}
```

---

## Step 4: Track Order

After receiving **202 Accepted**, poll the order until status is `distribution_completed` or `distribution_failed`:

```bash
curl -s "https://x402.crosstoken.io/orders/YOUR_ORDER_ID" | jq .
```

Typical flow: `payment_verified` → `distribution_completed` (or `distribution_failed`). Use the `order_id` from the 202 response.

---

## Switching to Production

1. Change the base URL to `https://x402.crosstoken.io`.
2. Use **USDC on Base mainnet** (chain ID 8453). The SDK will use the same facilitator; the server will return payment requirements for Base mainnet when you call the production URL.

No code changes besides the base URL and ensuring the wallet has mainnet USDC.

---

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| **402 then failure** | Ensure the private key matches a wallet that holds enough USDC on the correct network (Base Sepolia for testnet, Base for production). |
| **429 Rate limited** | Reduce request rate; wait and retry. |
| **400 / 422** | Validate `distribution_amount` (wei string), `recipient` (valid 0x address). Do not send both `payment_amount` and `distribution_amount` to `/rates`. |
| **503** | Server or pricing temporarily unavailable; retry later. |
| **No scheme registered** (SDK) | The 402 response asks for a network (e.g. `eip155:84532`). Ensure you registered the EVM scheme with `eip155:*` (or the specific chain) in your x402 client. |

For full API reference and error codes, see [x402-skill.md](x402-skill.md).
