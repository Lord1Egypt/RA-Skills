---
name: ntriq-x402-screenshot-data-batch
description: "Batch extract text, UI elements, and data from up to 500 screenshots. Flat $6.00 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [screenshot, ui, batch, extraction, vision, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Screenshot Data Batch (x402)

Extract text, UI elements, layout structure, and data tables from up to 500 screenshots in one call. Flat $6.00 USDC. 100% local inference on Mac Mini.

## How to Call

```bash
POST https://x402.ntriq.co.kr/screenshot-data-batch
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "images": [
    "https://example.com/screen1.png",
    "https://example.com/screen2.png"
  ],
  "extract_type": "full"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `images` | array | ✅ | Screenshot URLs (max 500) |
| `extract_type` | string | ❌ | `full` \| `text` \| `data` (default: `full`) |
| `language` | string | ❌ | Output language (default: `en`) |

## Example Response

```json
{
  "status": "ok",
  "count": 2,
  "results": [
    {
      "image_url": "https://example.com/screen1.png",
      "status": "ok",
      "extract_type": "full",
      "analysis": "Dashboard showing sales metrics: Total Revenue $124,500, Active Users 3,421..."
    }
  ]
}
```

## Payment

- **Price**: $6.00 USDC flat (up to 500 screenshots)
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
