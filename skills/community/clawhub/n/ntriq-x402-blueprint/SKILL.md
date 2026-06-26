---
name: ntriq-x402-blueprint
description: "AI architectural blueprint analysis — extract rooms, dimensions, materials from floor plans. $0.05 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [blueprint, architecture, vision, construction, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Blueprint Intelligence (x402)

Extract structured data from architectural blueprints and floor plans — room names, dimensions, areas, materials, and structural elements. Uses local vision AI. $0.05 USDC per call.

## How to Call

```bash
POST https://x402.ntriq.co.kr/blueprint
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "image_url": "https://example.com/floorplan.jpg",
  "analysis_type": "full"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image_url` | string | ✅ (or base64) | Blueprint image URL |
| `image_base64` | string | ✅ (or url) | Base64-encoded image |
| `analysis_type` | string | ❌ | `full` \| `dimensions` \| `rooms` \| `materials` (default: `full`) |
| `language` | string | ❌ | Output language (default: `en`) |

## Example Response

```json
{
  "status": "ok",
  "analysis_type": "full",
  "rooms": [
    {"name": "Living Room", "area": "24 m²", "dimensions": "6m × 4m"},
    {"name": "Kitchen", "area": "12 m²", "dimensions": "4m × 3m"}
  ],
  "total_area": "85 m²",
  "scale": "1:100",
  "structural_elements": ["load-bearing wall", "steel beam"],
  "notes": "3-bedroom apartment, ground floor"
}
```

## Payment

- **Price**: $0.05 USDC per call
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
