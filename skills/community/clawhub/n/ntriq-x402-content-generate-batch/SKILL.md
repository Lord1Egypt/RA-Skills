---
name: ntriq-x402-content-generate-batch
description: "Batch AI content generation for up to 500 prompts. Flat $6.00 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [content, writing, batch, nlp, generation, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Content Generate Batch (x402)

Generate content for up to 500 prompts in a single call. Flat $6.00 USDC. 100% local inference on Mac Mini.

## How to Call

```bash
POST https://x402.ntriq.co.kr/content-generate-batch
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "prompts": [
    "benefits of standing desks",
    "best practices for remote meetings",
    "how to improve team productivity"
  ],
  "style": "blog",
  "tone": "professional",
  "max_words": 300
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompts` | array | ✅ | Content topics (max 500) |
| `style` | string | ❌ | `blog` \| `email` \| `social` \| `product` \| `report` \| `ad` |
| `tone` | string | ❌ | `professional` \| `casual` \| `persuasive` \| `friendly` |
| `language` | string | ❌ | Output language (default: `en`) |
| `max_words` | integer | ❌ | Max words per item (default: 500) |

## Payment

- **Price**: $6.00 USDC flat (up to 500 prompts)
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
