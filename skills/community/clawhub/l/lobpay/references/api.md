# LobPay API Reference

## Base URL
```
http://localhost:3000/api/v1  (dev)
https://lobpay.market/api/v1  (prod)
```

---

## Public Endpoints

### GET /public/checkout-info

Retrieve pricing and merchant wallet for a product.

**Query Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| product_id | integer | Yes | Product ID |
| quantity | integer | No | Quantity (default: 1) |

**Response:**
```json
{
  "product_name": "Premium Widget",
  "unit_price": "10.00",
  "total_amount": "20.00",
  "currency": "USD",
  "merchant_wallet": "0x1234...",
  "merchant_name": "Acme Corp",
  "network": "eip155:84532"
}
```

---

## Authenticated Endpoints

All require header: `Authorization: Bearer {api_key}`

### POST /agents/purchase

Execute a purchase with X402 payment.

**Request Body:**
```json
{
  "items": [
    { "product_id": 101, "quantity": 2 }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "transaction_id": 123,
  "recorded_hash": "0xabc...",
  "total_amount": "20.00",
  "message": "Transaction recorded successfully"
}
```

**X402 Flow:**
1. Client sends request with API key
2. Server responds with `402 Payment Required` + X402 headers
3. Client signs payment header with private key
4. Client resends with `X-Payment` header
5. Server settles on-chain and records transaction

---

### POST /agents/feedback

Leave rating and comment for a transaction.

**Request Body:**
```json
{
  "transaction_id": 123,
  "rating": 5,
  "comment": "Excellent service!",
  "status": "confirmed"
}
```

**Response:**
```json
{
  "success": true,
  "feedback_id": 456,
  "message": "Feedback recorded"
}
```

**Rating Scale:**
- 1-5 stars
- Must be integer
- Required field

---

### GET /agents/history

View purchase history (optional endpoint).

**Response:**
```json
{
  "transactions": [
    {
      "transaction_id": 123,
      "recorded_hash": "0xabc...",
      "total_amount": "20.00",
      "created_at": "2026-02-25T10:00:00Z"
    }
  ]
}
```

---

## Error Codes

| Status | Code | Description |
|--------|------|-------------|
| 400 | INVALID_PARAMS | Missing or invalid parameters |
| 401 | UNAUTHORIZED | Invalid or missing API key |
| 402 | PAYMENT_REQUIRED | X402 payment needed |
| 404 | NOT_FOUND | Product or transaction not found |
| 409 | ALREADY_RATED | Feedback already submitted |
| 500 | SERVER_ERROR | Internal server error |

---

## X402 Protocol Headers

### Challenge Response (402)
```http
HTTP/1.1 402 Payment Required
X-Payment-Version: x402-1.0
X-Payment-Chain: eip155:84532
X-Payment-Amount: 2000000
X-Payment-Token: 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
X-Payment-Pay-To: 0xMerchantWallet...
X-Payment-Required-At: 2026-02-25T10:00:00Z
```

### Payment Header
```http
X-Payment: eip155:84532;0xSignedPaymentHeader
```
