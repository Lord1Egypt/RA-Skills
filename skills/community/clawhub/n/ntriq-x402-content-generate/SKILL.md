---
name: ntriq-x402-content-generate
description: "AI content generation for blogs, emails, social posts, product descriptions. $0.02 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [content, writing, nlp, generation, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Content Generate (x402)

Generate professional content — blog posts, emails, social media, product descriptions, reports, and ad copy. 100% local inference on Mac Mini. $0.02 USDC per call.

## How to Call

```bash
POST https://x402.ntriq.co.kr/content-generate
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "prompt": "benefits of standing desks for office workers",
  "style": "blog",
  "tone": "professional",
  "max_words": 500
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | ✅ | Topic or content brief |
| `style` | string | ❌ | `blog` \| `email` \| `social` \| `product` \| `report` \| `ad` (default: `blog`) |
| `tone` | string | ❌ | `professional` \| `casual` \| `persuasive` \| `friendly` (default: `professional`) |
| `language` | string | ❌ | Output language (default: `en`) |
| `max_words` | integer | ❌ | Max word count (default: 500) |

## Example Response

```json
{
  "status": "ok",
  "style": "blog",
  "title": "5 Reasons Standing Desks Transform Office Productivity",
  "content": "Standing desks have revolutionized...",
  "word_count": 487
}
```

## Payment

- **Price**: $0.02 USDC per call
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
