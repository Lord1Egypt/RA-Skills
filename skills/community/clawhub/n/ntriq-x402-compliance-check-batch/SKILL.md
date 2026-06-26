---
name: ntriq-x402-compliance-check-batch
description: "Batch compliance analysis for up to 500 texts. Flat $9.00 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [compliance, legal, risk, batch, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Compliance Check Batch (x402)

Analyze up to 500 text inputs for compliance violations in one call. Flat $9.00 USDC. 100% local inference on Mac Mini.

## How to Call

```bash
POST https://x402.ntriq.co.kr/compliance-check-batch
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "texts": [
    "We collect user emails for marketing without explicit consent.",
    "All data is encrypted at rest using AES-256."
  ],
  "framework": "GDPR",
  "jurisdiction": "EU"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `texts` | array | ✅ | Texts to analyze (max 500) |
| `framework` | string | ❌ | `GDPR` \| `HIPAA` \| `SOX` \| `general` |
| `jurisdiction` | string | ❌ | `US` \| `EU` \| `UK` etc. |
| `language` | string | ❌ | Output language (default: `en`) |

## Payment

- **Price**: $9.00 USDC flat (up to 500 texts)
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
