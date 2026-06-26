---
name: ntriq-x402-pii-detect
description: "Detect and optionally mask PII (emails, phone numbers, SSNs, names, addresses, credit cards) in text. Pay $0.02 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [pii, privacy, gdpr, compliance, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# PII Detection (x402)

Detect personally identifiable information in text — emails, phone numbers, SSNs, names, addresses, credit cards, passport numbers. Optionally mask detected PII. Returns risk level and exact positions. Pay $0.02 USDC per call via x402 (Base mainnet).

## How to Call

```bash
POST https://x402.ntriq.co.kr/pii-detect
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "text": "Contact John Smith at john.smith@email.com or 555-123-4567",
  "mask": false
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | ✅ | Text to analyze for PII |
| `mask` | boolean | ❌ | Replace PII with `[TYPE]` placeholders (default: `false`) |

## PII Types Detected

`email`, `phone`, `ssn`, `name`, `address`, `credit_card`, `passport`, `other`

## Risk Levels

`none`, `low`, `medium`, `high`, `critical`

## Example Response

```json
{
  "status": "ok",
  "pii_found": [
    {"type": "name", "value": "John Smith", "position": [8, 18]},
    {"type": "email", "value": "john.smith@email.com", "position": [22, 42]},
    {"type": "phone", "value": "555-123-4567", "position": [46, 58]}
  ],
  "risk_level": "high",
  "masked_text": null
}
```

With `mask: true`:
```json
{
  "masked_text": "Contact [NAME] at [EMAIL] or [PHONE]",
  "risk_level": "high"
}
```

## Payment

- **Price**: $0.02 USDC per call
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
