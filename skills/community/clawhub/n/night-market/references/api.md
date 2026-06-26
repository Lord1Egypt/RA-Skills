# Nightmarket API Reference

Everything is standard HTTP. No SDK, no special client — just curl.

## Search & Discovery

### List / search services

```
GET https://nightmarket.ai/api/marketplace
GET https://nightmarket.ai/api/marketplace?search=<query>
```

**Query parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `search` | string | — | Filter by name, description, or seller (case-insensitive) |

Results are sorted by popularity (total calls, descending).

**Response:** JSON array of services

```json
[
  {
    "_id": "jn712kazdeyyyw3sk6m2qdy68d82gh1w",
    "type": "service",
    "name": "Fallom Labs",
    "description": "A wide variety of Agent skills",
    "endpointCount": 21,
    "priceRange": { "min": 0.0001, "max": 0.5 },
    "totalCalls": 14,
    "totalRevenue": 0.84,
    "seller": {
      "_id": "jd7bpe5v112dkqgbp4yq2nrr998229hv",
      "companyName": "Fallom Labs",
      "description": "A wide variety of Agent skills",
      "isVerified": false
    }
  }
]
```

Each item is a **service** — a group of endpoints from one seller. Use the service `_id` to get full details.

### Get service details (all endpoints)

```
GET https://nightmarket.ai/api/marketplace/service/<service_id>
```

**Response:** service object with its full endpoint list

```json
{
  "_id": "jn712kazdeyyyw3sk6m2qdy68d82gh1w",
  "name": "Fallom Labs",
  "description": "A wide variety of Agent skills",
  "totalCalls": 14,
  "totalRevenue": 0.84,
  "seller": {
    "companyName": "Fallom Labs",
    "isVerified": false,
    "createdAt": 1773004500574
  },
  "endpoints": [
    {
      "_id": "endpoint_abc123",
      "name": "Sentiment Analysis",
      "description": "Analyze text sentiment",
      "method": "POST",
      "priceUsdc": 0.01,
      "totalCalls": 5,
      "totalRevenue": 0.05,
      "requestExample": "{\"text\": \"I love this product\"}",
      "responseExample": "{\"sentiment\": \"positive\", \"confidence\": 0.95}"
    }
  ]
}
```

Returns 404 if the service doesn't exist or is inactive.

### Get single endpoint details

```
GET https://nightmarket.ai/api/marketplace/<endpoint_id>
```

Returns a single endpoint with its seller info, request/response examples, and parent service (if any). Useful when you already know the endpoint ID.

Returns 404 if the endpoint doesn't exist or is inactive.

---

## Calling Endpoints

### Proxy URL

```
<METHOD> https://nightmarket.ai/api/x402/<endpoint_id>
```

- `METHOD`: GET, POST, PUT, PATCH, or DELETE (must match what the endpoint expects)
- `endpoint_id`: the endpoint's `_id` from the service details response

Important: you call **endpoints**, not services. Get the endpoint `_id` from the service details response.

### Request Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Content-Type` | For POST/PUT/PATCH | Usually `application/json` |
| `Authorization` | If endpoint requires it | Passed through to the seller's API |
| `payment-signature` | After 402 | Signed x402 payment proof |

### Request Body

Pass the body exactly as the endpoint expects it. The proxy forwards it unchanged.

---

## Payment Flow

### Free endpoints (priceUsdc = 0)

Free endpoints skip payment entirely. Your request goes straight through to the seller's API and you get the response immediately.

### Paid endpoints — First call → 402 Payment Required

Every first call to a paid endpoint returns 402. This is normal — it's how x402 works.

**Response headers:**
- `PAYMENT-REQUIRED`: encoded payment requirements containing:
  - `scheme`: "exact"
  - `payTo`: seller's payment address (on Base)
  - `price`: amount in USDC (e.g., "$0.01")
  - `network`: "base"

**Response body:** `{}`

### Retry with payment → Success

Resend the exact same request with the payment proof.

**Add this header:**
- `payment-signature`: your signed x402 payment proof

**Successful response headers:**
- `PAYMENT-RESPONSE`: settlement proof containing `txHash` (on-chain transaction hash)
- `x-request-id`: unique request ID for debugging

**Successful response body:** the seller's API response, passed through unchanged.

---

## Error Codes

| Status | Meaning | Action |
|--------|---------|--------|
| 200-299 | Success | Response body is the API result |
| 400 | Invalid endpoint ID or bad payment signature | Check your endpoint_id and payment format |
| 402 | Payment required | Normal for paid endpoints — sign payment and retry |
| 402 (after payment) | Payment verification or settlement failed | Check wallet balance, verify signature |
| 403 | Endpoint URL blocked | Internal safety check — seller's URL not allowed |
| 404 | Endpoint not found or inactive | Service may have been removed |
| 500 | Internal server error | Nightmarket issue — try again later |
| 502 | Seller's API unreachable or timed out | The seller's backend is down — try later |
| 503 | Seller payment not configured or settlement failed | Seller hasn't set up their payout wallet, or payment failed after retries |

All error responses include an `x-request-id` header for debugging.

---

## Complete Examples

### Browse → Get details → Call

```bash
# 1. Search for crypto APIs
curl -s "https://nightmarket.ai/api/marketplace?search=crypto"

# 2. Get full service details (all endpoints with examples)
curl -s "https://nightmarket.ai/api/marketplace/service/jn7bm8w1g2vg6ngqpjw8cjx41182gjbp"

# 3. Call an endpoint (first attempt — will get 402 for paid)
curl -i -X GET "https://nightmarket.ai/api/x402/endpoint_id_here"
# HTTP/2 402
# PAYMENT-REQUIRED: <encoded payment details>

# 4. Call it again with payment
curl -X GET "https://nightmarket.ai/api/x402/endpoint_id_here" \
  -H "payment-signature: <signed payment>"
# HTTP/2 200
# PAYMENT-RESPONSE: <settlement proof>
# {"pumps": [...], "alerts": [...]}
```

### POST request with body

```bash
curl -i -X POST "https://nightmarket.ai/api/x402/def456" \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product"}'
# HTTP/2 402

curl -X POST "https://nightmarket.ai/api/x402/def456" \
  -H "Content-Type: application/json" \
  -H "payment-signature: <signed payment>" \
  -d '{"text": "I love this product"}'
# HTTP/2 200
# {"sentiment": "positive", "confidence": 0.95}
```

### Calling a free endpoint

```bash
# Free endpoints work immediately — no 402, no payment
curl -X GET "https://nightmarket.ai/api/x402/free_endpoint_id"
# HTTP/2 200
# {"result": "..."}
```

## Rate Limits & Timeouts

- **Proxy timeout:** 30 seconds per request
- **No rate limits** from Nightmarket (individual sellers may have their own)
- **Payment:** each call is independent — no sessions or tokens to manage
- **Settlement:** paid calls include up to 3 automatic retry attempts for on-chain settlement
