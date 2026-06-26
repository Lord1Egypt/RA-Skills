---
name: ntriq-x402-alt-text
description: "Generate WCAG-compliant alt text and detailed image descriptions for accessibility. Pay $0.01 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [accessibility, alt-text, wcag, vision, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Alt Text Generator (x402)

Generate concise WCAG-compliant alt text (≤125 chars) and a detailed accessibility description for any image. Ideal for agents processing image libraries, CMS content, or e-commerce product photos. Pay $0.01 USDC per call via x402 (Base mainnet).

## How to Call

```bash
POST https://x402.ntriq.co.kr/alt-text
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "image_url": "https://example.com/product.jpg"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image_url` | string | ✅ (or base64) | URL of image |
| `image_base64` | string | ✅ (or url) | Base64-encoded image |
| `language` | string | ❌ | Output language (default: `en`) |

## Example Response

```json
{
  "status": "ok",
  "alt_text": "Red leather office chair with adjustable armrests on wheels",
  "description": "A high-back executive office chair upholstered in red genuine leather. The chair features padded armrests, lumbar support, and a five-star wheeled base suitable for hard floors."
}
```

## Payment

- **Price**: $0.01 USDC per call
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
