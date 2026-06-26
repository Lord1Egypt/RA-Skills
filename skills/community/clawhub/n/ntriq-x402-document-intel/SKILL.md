---
name: ntriq-x402-document-intel
description: "Extract text, classify document type, and pull tables from any document image. Pay $0.05 USDC per call via x402 (no API key needed)."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [document, ocr, extraction, x402, vision]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Document Intelligence (x402)

Analyze document images — invoices, contracts, forms, reports — with local AI vision. Extracts text, classifies document type, pulls tables, or summarizes. No cloud upload, no API key. Pay $0.05 USDC per call via x402 micropayment (Base mainnet).

## How to Call

```bash
POST https://x402.ntriq.co.kr/document-intel
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "image_url": "https://example.com/document.png",
  "analysis_type": "extract"
}
```

The server responds with `402 Payment Required` first. Sign the EIP-3009 payment payload and retry with `X-PAYMENT` header.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image_url` | string | ✅ (or base64) | Publicly accessible URL of document image |
| `image_base64` | string | ✅ (or url) | Base64-encoded document image |
| `analysis_type` | string | ❌ | `extract` (default), `summarize`, `classify`, `table` |
| `language` | string | ❌ | Output language ISO code (default: `en`) |

## analysis_type Options

| Value | What it does |
|-------|-------------|
| `extract` | Full text extraction preserving structure |
| `summarize` | Key points, dates, amounts, parties |
| `classify` | Document type + key metadata |
| `table` | All tables as JSON array |

## Example Response

```json
{
  "status": "ok",
  "analysis_type": "classify",
  "analysis": "invoice",
  "confidence": 0.97,
  "metadata": {
    "vendor": "Acme Supplies Ltd.",
    "invoice_number": "INV-2024-0847",
    "date": "2024-03-15",
    "total": "$475.00"
  }
}
```

## Payment

- **Price**: $0.05 USDC per call
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)
- **Wallet**: `0x124AaFfF8Ef45F2cA953807aF09Aacec2D9F8307`

```bash
# Service catalog
curl https://x402.ntriq.co.kr/services
```
