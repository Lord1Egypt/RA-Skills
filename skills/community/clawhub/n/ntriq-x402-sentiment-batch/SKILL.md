---
name: ntriq-x402-sentiment-batch
description: "Batch sentiment and intent analysis for up to 500 texts. Flat $3.00 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [sentiment, nlp, batch, analysis, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Sentiment Batch (x402)

Analyze sentiment, emotions, and intent across up to 500 text inputs in one call. Returns confidence scores, emotion breakdown, and intent classification. Flat $3.00 USDC. 100% local inference on Mac Mini.

## How to Call

```bash
POST https://x402.ntriq.co.kr/sentiment-batch
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "texts": [
    "This product exceeded my expectations!",
    "Delivery was late and packaging was damaged."
  ],
  "language": "en"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `texts` | array | ✅ | Text strings to analyze (max 500) |
| `language` | string | ❌ | Output language (default: `en`) |

## Example Response

```json
{
  "status": "ok",
  "count": 2,
  "results": [
    {
      "index": 0,
      "status": "ok",
      "sentiment": "positive",
      "confidence": 0.95,
      "intent": "praise",
      "summary": "Customer is highly satisfied with the product quality."
    },
    {
      "index": 1,
      "status": "ok",
      "sentiment": "negative",
      "confidence": 0.88,
      "intent": "complain",
      "summary": "Customer complaints about late delivery and damaged packaging."
    }
  ]
}
```

## Payment

- **Price**: $3.00 USDC flat (up to 500 texts)
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
