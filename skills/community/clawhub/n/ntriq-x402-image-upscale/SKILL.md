---
name: ntriq-x402-image-upscale
description: "AI image upscaling using Real-ESRGAN. 2x/3x/4x super-resolution for photos and general images. $0.10 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [image, upscale, esrgan, super-resolution, vision, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Image Upscale (x402)

AI-powered image super-resolution using Real-ESRGAN on Apple M4 GPU. Upscale images 2x, 3x, or 4x with dramatic quality improvement. Supports jpg, png, webp. $0.10 USDC per image.

## How to Call

```bash
POST https://x402.ntriq.co.kr/image-upscale
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "image_url": "https://example.com/low-res.jpg",
  "scale": 4,
  "mode": "general"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image_url` | string | ✅ (or base64) | URL of image to upscale (jpg/png/webp) |
| `image_base64` | string | ✅ (or url) | Base64-encoded image |
| `scale` | integer | ❌ | Upscale factor: `2`, `3`, or `4` (default: `4`) |
| `mode` | string | ❌ | `general` (default) or `photo` (optimized for real-world photos, always 4x) |

## Example Response

```json
{
  "status": "ok",
  "scale": 4,
  "model": "realesr-animevideov3-x4",
  "image_base64": "<base64-encoded-png>",
  "format": "png"
}
```

## Payment

- **Price**: $0.10 USDC per call
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
