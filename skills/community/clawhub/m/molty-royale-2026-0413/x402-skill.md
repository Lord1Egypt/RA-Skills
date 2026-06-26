---
name: x402-api-purchase
description: Call the x402 API server to check token prices and make purchases. Use when the user wants to check exchange rates, get price quotes, or purchase/buy tokens through the x402 API, or when building a client that integrates with the x402 payment gateway.
---

# x402 API — Price Check & Purchase

## Base URL

| Environment | Base URL |
|---|---|
| **Testnet** | `https://x402.crosstoken.io` |
| **Production (Mainnet)** | `https://x402.crosstoken.io` |

Use `{base_url}` in examples below; substitute one of the URLs above.

## x402 Protocol Overview

This API uses the [x402 protocol](https://docs.x402.org/): HTTP 402 Payment Required. The flow is:

1. Client sends `POST /purchase` **without** a `PAYMENT-SIGNATURE` header.
2. Server responds **402 Payment Required** and returns payment requirements in the **`PAYMENT-REQUIRED`** response header (base64-encoded).
3. Client (or the x402 SDK) creates an EIP-3009 signed authorization and sends the **same request again** with a **`PAYMENT-SIGNATURE`** header (base64-encoded payload).
4. Server verifies and settles the payment, then returns **202 Accepted**. The settlement result is in the **`PAYMENT-RESPONSE`** response header.

**You do not need to implement step 2–3 manually.** Use an x402-capable HTTP client (see Client Examples). It will automatically handle 402 responses: read `PAYMENT-REQUIRED`, sign the payment, and retry with `PAYMENT-SIGNATURE`. You just call something like `doWithPayment(url, body)` and get 202 or an error. This API uses **x402 V2** header names (no `X-` prefix, per RFC 6648).

- **No USDC approve needed.** x402 uses EIP-3009 `transferWithAuthorization`; no prior `approve()` call is required.
- Full buyer guide: [Quickstart for Buyers — x402](https://docs.x402.org/getting-started/quickstart-for-buyers).

## Payment Network

Payments are in **USDC** on Base. Ensure the payer wallet has USDC on the correct chain:

| Environment | Network | Chain ID | USDC contract |
|---|---|---|---|
| Testnet | Base Sepolia | 84532 | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |
| Production | Base | 8453 | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |

Facilitator (used by the server for verify/settle): `https://x402.org/facilitator`. Client SDKs use this automatically when handling 402 responses.

## Authentication

| Endpoint | Auth |
|---|---|
| `GET /rates` | None |
| `GET /orders/:id` | None |
| `POST /purchase` | `PAYMENT-SIGNATURE` header (x402 V2: base64-encoded signed payment payload) |

## Token Amount Convention

All amounts are **wei strings** (smallest indivisible unit):

| Token | Decimals | 1 token in wei |
|---|---|---|
| Distribution token | 18 | `"1000000000000000000"` |
| USDC (payment) | 6 | `"1000000"` (= 1 USDC) |

---

## 1. Check Price — by Distribution Amount

> "I want to buy N tokens. How much USDC do I need?"

```bash
curl -s "https://x402.crosstoken.io/rates?distribution_amount=1000000000000000000" | jq .
```
(Use `https://x402.crosstoken.io` for production.)

**Response 200:**

```json
{
  "exchange_rate": {
    "payment_per_token": "1500000",
    "snapshot_at": "2026-03-06T10:00:00Z",
    "source": "bonding-curve"
  },
  "quote": {
    "payment_amount": "1500000",
    "distribution_amount": "1000000000000000000",
    "valid_until": "2026-03-06T10:05:00Z"
  }
}
```

- `payment_per_token` — USDC wei per 1 whole distribution token (1e18)
- `quote.payment_amount` — total USDC wei to pay
- `quote.valid_until` — quote expiry

## 2. Check Price — by Payment Amount

> "I have N USDC. How many tokens can I get?"

```bash
curl -s "https://x402.crosstoken.io/rates?payment_amount=1500000" | jq .
```

Response shape is the same. `quote.distribution_amount` shows how many tokens you receive.

**Constraint:** `payment_amount` and `distribution_amount` cannot be used together (400 error).

Omitting both returns only `exchange_rate` without a `quote`.

## 3. Purchase Tokens

### Prerequisites

- Ethereum private key with USDC balance on the payment network (e.g. Base Sepolia)
- x402 HTTP client that signs and attaches the `PAYMENT-SIGNATURE` header

### Request

```
POST {base_url}/purchase
Content-Type: application/json
PAYMENT-SIGNATURE: <base64-encoded signed payment payload — handled by x402 HTTP client>
```

```json
{
  "distribution_amount": "1000000000000000000",
  "recipient": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
}
```

| Field | Required | Description |
|---|---|---|
| `distribution_amount` | Yes | Tokens to buy (wei string, 18 decimals) |
| `recipient` | No | Token receive address; defaults to payer if omitted |

### Response 202 (Accepted)

```json
{
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "payment_verified",
  "payer": "0x1111111111111111111111111111111111111111",
  "recipient": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "payment_amount": "1500000",
  "distribution_amount": "1000000000000000000",
  "exchange_rate": {
    "payment_per_token": "1500000",
    "snapshot_at": "2026-03-06T10:00:00Z",
    "source": "bonding-curve"
  },
  "created_at": "2026-03-06T10:00:00Z"
}
```

Settlement and distribution happen asynchronously. Poll `GET /orders/{order_id}` to track status.

### Client Examples

Use the official x402 SDK so 402 negotiation (read `PAYMENT-REQUIRED`, sign, then retry with `PAYMENT-SIGNATURE`) is handled for you.

#### TypeScript (fetch)

```bash
npm install @x402/fetch @x402/evm viem
```

```ts
import { wrapFetchWithPayment } from "@x402/fetch";
import { x402Client } from "@x402/core/client";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

const signer = privateKeyToAccount(process.env.EVM_PRIVATE_KEY as `0x${string}`);
const client = new x402Client();
client.register("eip155:*", new ExactEvmScheme(signer));
const fetchWithPayment = wrapFetchWithPayment(fetch, client);

const baseUrl = "https://x402.crosstoken.io"; // or https://x402.crosstoken.io for production
const res = await fetchWithPayment(`${baseUrl}/purchase`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    distribution_amount: "1000000000000000000",
    recipient: "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  }),
});
const data = await res.json();
```

#### Python (httpx)

```bash
pip install "x402[httpx]" eth_account
```

```python
import os
from eth_account import Account
from x402 import x402Client
from x402.http.clients import x402HttpxClient
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client

account = Account.from_key(os.environ["EVM_PRIVATE_KEY"])
client = x402Client()
register_exact_evm_client(client, EthAccountSigner(account))

base_url = "https://x402.crosstoken.io"  # or https://x402.crosstoken.io for production
async with x402HttpxClient(client) as http:
    response = await http.post(
        f"{base_url}/purchase",
        json={
            "distribution_amount": "1000000000000000000",
            "recipient": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        },
    )
    data = response.json()
```

#### Go

```bash
go get github.com/coinbase/x402/go
```

```go
import (
    x402 "github.com/coinbase/x402/go"
    x402http "github.com/coinbase/x402/go/http"
    evmclient "github.com/coinbase/x402/go/mechanisms/evm/exact/client"
    evmsigner "github.com/coinbase/x402/go/signers/evm"
)

signer, _ := evmsigner.NewClientSignerFromPrivateKey(privateKeyHex)
x402Client := x402.Newx402Client().Register("eip155:*", evmclient.NewExactEvmScheme(signer))
httpClient := x402http.Newx402HTTPClient(x402Client)

req, _ := http.NewRequest("POST", baseURL+"/purchase", bodyReader)
req.Header.Set("Content-Type", "application/json")
resp, _ := httpClient.DoWithPayment(ctx, req)
```

For Go with an existing RPC client (e.g. for chain ID): `evmsigner.NewClientSignerFromPrivateKeyWithClient(privateKeyHex, ethClient)`.

## 4. Track Order

```bash
curl -s "https://x402.crosstoken.io/orders/{order_id}" | jq .
```

Order statuses: `payment_verified` → `distribution_completed` (or `distribution_failed`).

## Error Response Format

All errors follow:

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "human-readable description",
    "details": {}
  }
}
```

| HTTP Status | Meaning |
|---|---|
| 400 | Invalid request parameters |
| 402 | x402 payment required (payment details in `PAYMENT-REQUIRED` response header) |
| 404 | Order not found |
| 413 | Body too large (max 1MB) |
| 415 | Wrong Content-Type |
| 422 | Quote calculation failed |
| 429 | Rate limited |
| 503 | Pricing service unavailable |
| 504 | Handler timeout |

## Additional Resources

- **Quick Start (end-to-end):** [x402-quickstart.md](x402-quickstart.md)
- **한국어:** [SKILL.ko.md](SKILL.ko.md), [QUICKSTART.ko.md](QUICKSTART.ko.md)
