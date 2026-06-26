---
name: ntriq-x402-sentiment
description: "Analyze sentiment, emotions (joy/anger/sadness/fear), and intent from any text. Pay $0.01 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [sentiment, nlp, emotion, intent, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Sentiment Analysis (x402)

Analyze sentiment, emotion breakdown, and intent from any text. Returns structured scores for joy, anger, sadness, fear, surprise, and disgust — plus intent classification and a one-sentence summary. Pay $0.01 USDC per call via x402 (Base mainnet).

## How to Call

```bash
POST https://x402.ntriq.co.kr/sentiment
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "text": "I've been waiting 3 weeks and still no response. This is completely unacceptable.",
  "language": "en"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | ✅ | Text to analyze |
| `language` | string | ❌ | Response language ISO code (default: `en`) |

## Example Response

```json
{
  "status": "ok",
  "sentiment": "negative",
  "confidence": 0.94,
  "emotions": {
    "joy": 0.02,
    "anger": 0.71,
    "sadness": 0.18,
    "fear": 0.05,
    "surprise": 0.02,
    "disgust": 0.62
  },
  "intent": "complain",
  "summary": "Customer expresses strong frustration over a 3-week delay without any response."
}
```

## Sentiment Values

`positive`, `negative`, `neutral`, `mixed`

## Intent Values

`inform`, `request`, `complain`, `praise`, `question`, `suggest`, `other`

## Payment

- **Price**: $0.01 USDC per call
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
