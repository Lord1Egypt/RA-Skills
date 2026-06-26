---
name: ntriq-x402-compliance-check
description: "AI compliance analysis for contracts, policies, and text. Detects issues and recommends fixes. $0.03 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [compliance, legal, risk, analysis, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Compliance Check (x402)

Analyze text for compliance issues across GDPR, HIPAA, SOX, general corporate policy, or custom frameworks. Returns risk level, specific violations, and remediation recommendations. $0.03 USDC per call.

## How to Call

```bash
POST https://x402.ntriq.co.kr/compliance-check
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "text": "We store user passwords in plain text and share data with third parties.",
  "framework": "GDPR",
  "jurisdiction": "EU"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | ✅ | Text to analyze |
| `framework` | string | ❌ | `GDPR` \| `HIPAA` \| `SOX` \| `general` (default: `general`) |
| `jurisdiction` | string | ❌ | `US` \| `EU` \| `UK` etc. (default: `US`) |
| `language` | string | ❌ | Output language (default: `en`) |

## Example Response

```json
{
  "status": "ok",
  "compliant": false,
  "risk_level": "critical",
  "issues": [
    {
      "rule": "GDPR Art. 32 - Security of processing",
      "description": "Plain text password storage violates security requirements",
      "severity": "critical",
      "recommendation": "Implement bcrypt or Argon2 password hashing"
    }
  ],
  "summary": "2 critical violations found requiring immediate remediation."
}
```

## Payment

- **Price**: $0.03 USDC per call
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
