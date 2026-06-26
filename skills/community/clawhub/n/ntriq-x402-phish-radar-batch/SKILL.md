---
name: ntriq-x402-phish-radar-batch
description: "Batch phishing detection for up to 500 URLs or domains. Flat $9.00 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [phishing, cybersecurity, threat, batch, domain, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Phish Radar Batch (x402)

Scan up to 500 URLs or domains for phishing in one call. Flat $9.00 USDC. Local AI inference on Mac Mini.

## How to Call

```bash
POST https://x402.ntriq.co.kr/phish-radar-batch
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "targets": [
    "https://paypa1.com/login",
    "https://amazon-security-update.net",
    "https://google.com"
  ]
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `targets` | array | ✅ | URLs or domains to scan (max 500) |
| `language` | string | ❌ | Output language (default: `en`) |

## Example Response

```json
{
  "status": "ok",
  "count": 3,
  "results": [
    {"index": 0, "target": "https://paypa1.com/login", "risk_level": "critical", "recommendation": "block"},
    {"index": 1, "target": "https://amazon-security-update.net", "risk_level": "high", "recommendation": "avoid"},
    {"index": 2, "target": "https://google.com", "risk_level": "safe", "recommendation": "safe_to_visit"}
  ]
}
```

## Payment

- **Price**: $9.00 USDC flat (up to 500 targets)
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
