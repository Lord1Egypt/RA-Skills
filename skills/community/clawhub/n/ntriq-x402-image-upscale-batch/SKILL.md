---
name: ntriq-x402-image-upscale-batch
description: "Batch AI image upscaling for up to 500 images using Real-ESRGAN. Flat $30.00 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [image, upscale, esrgan, super-resolution, batch, vision, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Image Upscale Batch (x402)

Upscale up to 500 images in one call using Real-ESRGAN on Apple M4 GPU. Flat $30.00 USDC.

## How to Call

```bash
POST https://x402.ntriq.co.kr/image-upscale-batch
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "images": [
    "https://example.com/img1.jpg",
    "https://example.com/img2.jpg"
  ],
  "scale": 4,
  "mode": "general"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `images` | array | ✅ | Image URLs to upscale (max 500, jpg/png/webp) |
| `scale` | integer | ❌ | Upscale factor: `2`, `3`, or `4` (default: `4`) |
| `mode` | string | ❌ | `general` (default) or `photo` (real-world photos, always 4x) |

## Payment

- **Price**: $30.00 USDC flat (up to 500 images)
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
