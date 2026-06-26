---
name: ntriq-x402-blueprint-batch
description: "Batch architectural blueprint analysis for up to 500 images. Flat $15.00 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [blueprint, architecture, batch, vision, construction, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Blueprint Batch (x402)

Analyze up to 500 architectural blueprints in one call. Flat $15.00 USDC. 100% local vision AI on Mac Mini.

## How to Call

```bash
POST https://x402.ntriq.co.kr/blueprint-batch
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "images": [
    "https://example.com/floor1.jpg",
    "https://example.com/floor2.jpg"
  ],
  "analysis_type": "rooms"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `images` | array | ✅ | Blueprint image URLs (max 500) |
| `analysis_type` | string | ❌ | `full` \| `dimensions` \| `rooms` \| `materials` |
| `language` | string | ❌ | Output language (default: `en`) |

## Payment

- **Price**: $15.00 USDC flat (up to 500 blueprints)
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
