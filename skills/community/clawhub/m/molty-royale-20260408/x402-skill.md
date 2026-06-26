---
name: x402-api-purchase
description: Call the x402 API server to check token prices and make purchases.
---

# x402 API — Price Check & Purchase

## Base URL

| Environment | Base URL |
|---|---|
| **Testnet** | `https://x402.crosstoken.io` |
| **Production (Mainnet)** | `https://x402.crosstoken.io` |

## x402 Protocol Overview

This API uses the [x402 protocol](https://docs.x402.org/): HTTP 402 Payment Required. The flow is:

1. Client sends `POST /purchase` **without** a `PAYMENT-SIGNATURE` header.
2. Server responds **402 Payment Required** and returns payment requirements in the **`PAYMENT-REQUIRED`** response header (base64-encoded).
3. Client (or the x402 SDK) creates an EIP-3009 signed authorization and sends the **same request again** with a **`PAYMENT-SIGNATURE`** header (base64-encoded payload).
4. Server verifies and settles the payment, then returns **202 Accepted**.

## Payment Network

| Environment | Network | Chain ID | USDC contract |
|---|---|---|---|
| Testnet | Base Sepolia | 84532 | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |
| Production | Base | 8453 | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |

## Authentication

| Endpoint | Auth |
|---|---|
| `GET /rates` | None |
| `GET /orders/:id` | None |
| `POST /purchase` | `PAYMENT-SIGNATURE` header (x402 V2) |

## Token Amount Convention

| Token | Decimals | 1 token in wei |
|---|---|---|
| Distribution token | 18 | `"1000000000000000000"` |
| USDC (payment) | 6 | `"1000000"` (= 1 USDC) |

---

## 1. Check Price — by Distribution Amount

```bash
curl -s "https://x402.crosstoken.io/rates?distribution_amount=1000000000000000000" | jq .
```

## 2. Check Price — by Payment Amount

```bash
curl -s "https://x402.crosstoken.io/rates?payment_amount=1500000" | jq .
```

## 3. Purchase Tokens

```
POST {base_url}/purchase
Content-Type: application/json
```

```json
{
  "distribution_amount": "1000000000000000000",
  "recipient": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
}
```

### Response 202 (Accepted)

```json
{
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "payment_verified",
  "payer": "0x1111111111111111111111111111111111111111",
  "recipient": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "payment_amount": "1500000",
  "distribution_amount": "1000000000000000000"
}
```

## 4. Track Order

```bash
curl -s "https://x402.crosstoken.io/orders/{order_id}" | jq .
```

## Error Response Format

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
| 402 | x402 payment required |
| 404 | Order not found |
| 422 | Quote calculation failed |
| 429 | Rate limited |
| 503 | Pricing service unavailable |

## Additional Resources

- **Quick Start:** [x402-quickstart.md](x402-quickstart.md)
