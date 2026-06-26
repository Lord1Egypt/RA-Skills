---
name: ntriq-x402-document-intel-batch
description: "Batch document OCR, classification, and extraction for up to 500 images. Flat $15.00 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [document, ocr, batch, extraction, vision, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Document Intelligence Batch (x402)

Process up to 500 document images in one call — OCR, classification, table extraction, and summarization. Flat $15.00 USDC. 100% local inference on Mac Mini.

## How to Call

```bash
POST https://x402.ntriq.co.kr/document-intel-batch
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "images": [
    "https://example.com/contract1.jpg",
    "https://example.com/report2.jpg"
  ],
  "analysis_type": "extract"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `images` | array | ✅ | Document image URLs (max 500) |
| `analysis_type` | string | ❌ | `extract` \| `summarize` \| `classify` \| `table` (default: `extract`) |
| `language` | string | ❌ | Output language (default: `en`) |

## Example Response

```json
{
  "status": "ok",
  "count": 2,
  "results": [
    {
      "image_url": "https://example.com/contract1.jpg",
      "status": "ok",
      "analysis_type": "extract",
      "analysis": "SERVICE AGREEMENT\nDate: January 15, 2026\nParties: ..."
    }
  ]
}
```

## Payment

- **Price**: $15.00 USDC flat (up to 500 documents)
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
