---
name: ntriq-vision-product-analyzer-mcp
description: "Analyze product images: identify items, extract specs, compare features, generate descriptions."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [product,vision,ecommerce]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Vision Product Analyzer MCP

Analyze product images to identify items, extract technical specifications, compare features across variants, and generate optimized product descriptions for e-commerce. Powered by local Qwen2.5-VL — no external API required.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `images` | array | ✅ | Product image URLs or base64 (up to 10 per product) |
| `tasks` | array | ❌ | `identify`, `specs`, `compare`, `description` (default: all) |
| `category_hint` | string | ❌ | Product category hint for better accuracy |
| `competitor_images` | array | ❌ | Competitor product images for comparison |

## Example Response

```json
{
  "product_identified": "Mechanical Gaming Keyboard",
  "category": "Computer Peripherals",
  "specifications": {
    "switch_type": "Cherry MX Red (visible through keycaps)",
    "form_factor": "TKL (Tenkeyless)",
    "backlight": "RGB per-key",
    "estimated_dimensions": "360mm x 130mm",
    "materials": ["aluminum top plate", "PBT keycaps"]
  },
  "description": "Compact tenkeyless mechanical keyboard with Cherry MX Red switches and per-key RGB backlighting. Aluminum top plate construction. Ideal for gaming and space-constrained setups.",
  "seo_tags": ["mechanical keyboard", "tkl keyboard", "cherry mx red", "rgb keyboard", "gaming keyboard"]
}
```

## Use Cases

- E-commerce catalog automation from manufacturer photos
- Product returns damage assessment
- Competitive product feature comparison research

## Access

```bash
# x402 endpoint — pay $0.05 USDC per call (Base mainnet)
POST https://x402.ntriq.co.kr/vision-product

# Service catalog
curl https://x402.ntriq.co.kr/services
```

[x402 micropayments](https://x402.ntriq.co.kr) — USDC on Base, gasless EIP-3009
