---
name: ntriq-x402-phish-radar
description: "Real-time phishing detection for URLs and domains. Risk scoring, brand impersonation detection. $0.03 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [phishing, cybersecurity, threat, domain, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Phish Radar (x402)

Detect phishing URLs and suspicious domains in real-time. Analyzes typosquatting, homoglyph attacks, brand impersonation, and DNS anomalies using local AI. $0.03 USDC per call.

## How to Call

```bash
POST https://x402.ntriq.co.kr/phish-radar
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "url": "https://paypa1.com/login"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | ✅ (or domain) | Full URL to analyze |
| `domain` | string | ✅ (or url) | Domain to analyze |
| `language` | string | ❌ | Output language (default: `en`) |

## Example Response

```json
{
  "status": "ok",
  "target": "https://paypa1.com/login",
  "is_suspicious": true,
  "risk_score": 92,
  "risk_level": "critical",
  "indicators": [
    {"type": "typosquatting", "description": "paypa1.com mimics paypal.com using digit '1' for letter 'l'"}
  ],
  "legitimate_brand": "PayPal",
  "recommendation": "block",
  "summary": "High-confidence PayPal phishing domain detected."
}
```

## Payment

- **Price**: $0.03 USDC per call
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
