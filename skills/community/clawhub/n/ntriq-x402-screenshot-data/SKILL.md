---
name: ntriq-x402-screenshot-data
description: "Convert screenshots into structured data — extract text, UI layout, tables, or charts from any screen image. Pay $0.02 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [screenshot, extraction, ui, vision, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Screenshot to Data (x402)

Turn any screenshot into structured data. Extract all visible text, analyze UI layout, pull tables and charts, or get full structured JSON. Useful for agents that need to process screen captures, dashboard screenshots, or web page images. Pay $0.02 USDC per call via x402 (Base mainnet).

## How to Call

```bash
POST https://x402.ntriq.co.kr/screenshot-data
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "image_url": "https://example.com/screenshot.png",
  "extract_type": "data"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image_url` | string | ✅ (or base64) | URL of screenshot |
| `image_base64` | string | ✅ (or url) | Base64-encoded screenshot |
| `extract_type` | string | ❌ | `full` (default), `text`, `layout`, `data` |
| `language` | string | ❌ | Output language (default: `en`) |

## extract_type Options

| Value | What it does |
|-------|-------------|
| `full` | All text, UI elements, layout, data as JSON |
| `text` | All visible text in reading order |
| `layout` | Navigation, buttons, forms, content areas |
| `data` | Tables, charts, numbers, structured info |

## Example Response

```json
{
  "status": "ok",
  "extract_type": "data",
  "analysis": {
    "tables": [
      {"headers": ["Month", "Revenue", "Users"], "rows": [["Jan", "$12,400", "340"], ["Feb", "$15,200", "412"]]}
    ],
    "charts": [{"type": "bar", "title": "Monthly Revenue", "trend": "increasing"}],
    "key_metrics": {"total_revenue": "$27,600", "total_users": 752}
  }
}
```

## Payment

- **Price**: $0.02 USDC per call
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
