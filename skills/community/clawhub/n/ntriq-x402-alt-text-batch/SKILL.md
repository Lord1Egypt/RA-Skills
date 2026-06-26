---
name: ntriq-x402-alt-text-batch
description: "Batch-generate WCAG-compliant alt text for up to 500 images in one call. Flat $3.00 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [accessibility, alt-text, batch, wcag, vision, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Alt Text Batch (x402)

Generate WCAG-compliant alt text and descriptions for up to 500 images in a single call. Flat $3.00 USDC — no per-image overhead. 100% local inference on Mac Mini.

## How to Call

```bash
POST https://x402.ntriq.co.kr/alt-text-batch
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "images": [
    "https://example.com/product1.jpg",
    "https://example.com/product2.jpg"
  ],
  "context": "e-commerce product catalog",
  "max_length": 125
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `images` | array | ✅ | Image URLs (max 500) |
| `context` | string | ❌ | Shared context for all images |
| `max_length` | integer | ❌ | Max chars per alt_text (default: 125) |
| `language` | string | ❌ | Output language (default: `en`) |

## Example Response

```json
{
  "status": "ok",
  "count": 2,
  "results": [
    {
      "image_url": "https://example.com/product1.jpg",
      "status": "ok",
      "alt_text": "Red leather office chair with adjustable armrests",
      "description": "A high-back executive office chair in red genuine leather with lumbar support."
    },
    {
      "image_url": "https://example.com/product2.jpg",
      "status": "ok",
      "alt_text": "Blue standing desk with cable management tray",
      "description": "An electric height-adjustable standing desk in matte blue finish."
    }
  ]
}
```

## Payment

- **Price**: $3.00 USDC flat (up to 500 images)
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
