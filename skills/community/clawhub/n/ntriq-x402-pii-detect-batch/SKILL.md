---
name: ntriq-x402-pii-detect-batch
description: "Batch detect and mask PII across up to 500 text inputs. Flat $6.00 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [pii, privacy, batch, compliance, security, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# PII Detect Batch (x402)

Detect and optionally mask Personally Identifiable Information (emails, phones, SSNs, names, addresses) across up to 500 text inputs in one call. Flat $6.00 USDC. 100% local inference on Mac Mini.

## How to Call

```bash
POST https://x402.ntriq.co.kr/pii-detect-batch
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "texts": [
    "Contact John Smith at john@example.com or 555-0123",
    "Invoice sent to 123 Main St, Springfield"
  ],
  "mask": true
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `texts` | array | ✅ | Text strings to analyze (max 500) |
| `mask` | boolean | ❌ | Replace PII with `[TYPE]` placeholders (default: `false`) |

## Example Response

```json
{
  "status": "ok",
  "count": 2,
  "results": [
    {
      "index": 0,
      "status": "ok",
      "pii_found": [
        {"type": "name", "value": "John Smith"},
        {"type": "email", "value": "john@example.com"},
        {"type": "phone", "value": "555-0123"}
      ],
      "risk_level": "high",
      "masked_text": "Contact [NAME] at [EMAIL] or [PHONE]"
    }
  ]
}
```

## Payment

- **Price**: $6.00 USDC flat (up to 500 texts)
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
