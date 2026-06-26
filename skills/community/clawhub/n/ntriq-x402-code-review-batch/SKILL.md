---
name: ntriq-x402-code-review-batch
description: "Batch AI code review for up to 500 snippets. Flat $15.00 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [code, review, security, batch, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Code Review Batch (x402)

Review up to 500 code snippets in a single call. Flat $15.00 USDC. 100% local inference on Mac Mini.

## How to Call

```bash
POST https://x402.ntriq.co.kr/code-review-batch
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "snippets": [
    "eval(userInput)",
    "password = 'hardcoded123'"
  ],
  "language": "javascript",
  "focus": "security"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `snippets` | array | ✅ | Code snippets to review (max 500) |
| `language` | string | ❌ | Programming language (default: `auto`) |
| `focus` | string | ❌ | `all` \| `security` \| `performance` \| `quality` |

## Payment

- **Price**: $15.00 USDC flat (up to 500 snippets)
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
