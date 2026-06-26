---
name: ntriq-x402-invoice-extract-batch
description: "Batch extract structured data from up to 500 invoices/receipts. Flat $9.00 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [invoice, receipt, batch, extraction, finance, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Invoice Extract Batch (x402)

Extract structured fields (vendor, amounts, line items, dates) from up to 500 invoice or receipt images in a single call. Flat $9.00 USDC. 100% local inference on Mac Mini.

## How to Call

```bash
POST https://x402.ntriq.co.kr/invoice-extract-batch
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "images": [
    "https://example.com/invoice1.jpg",
    "https://example.com/receipt2.jpg"
  ]
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `images` | array | ✅ | Invoice/receipt image URLs (max 500) |
| `language` | string | ❌ | Output language (default: `en`) |

## Example Response

```json
{
  "status": "ok",
  "count": 2,
  "results": [
    {
      "image_url": "https://example.com/invoice1.jpg",
      "status": "ok",
      "invoice": {
        "vendor_name": "Acme Corp",
        "invoice_number": "INV-2026-0042",
        "invoice_date": "2026-04-01",
        "total": 1250.00,
        "currency": "USD",
        "line_items": [{"description": "Consulting", "quantity": 10, "unit_price": 125, "amount": 1250}]
      }
    }
  ]
}
```

## Payment

- **Price**: $9.00 USDC flat (up to 500 invoices)
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
