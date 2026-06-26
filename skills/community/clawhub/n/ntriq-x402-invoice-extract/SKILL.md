---
name: ntriq-x402-invoice-extract
description: "Extract structured invoice data (vendor, line items, totals, tax) from any invoice image. Pay $0.03 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [invoice, extraction, accounting, x402, vision]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Invoice Extraction (x402)

Turn invoice or receipt images into structured JSON — vendor, customer, line items, tax, totals, payment terms. Local AI vision, no cloud upload, no API key. Pay $0.03 USDC per call via x402 (Base mainnet).

## How to Call

```bash
POST https://x402.ntriq.co.kr/invoice-extract
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "image_url": "https://example.com/invoice.jpg"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image_url` | string | ✅ (or base64) | URL of invoice/receipt image |
| `image_base64` | string | ✅ (or url) | Base64-encoded invoice image |
| `language` | string | ❌ | Output language (default: `en`) |

## Example Response

```json
{
  "status": "ok",
  "invoice": {
    "vendor_name": "Acme Supplies Ltd.",
    "vendor_address": "123 Main St, San Francisco, CA",
    "vendor_tax_id": "12-3456789",
    "invoice_number": "INV-2024-0847",
    "invoice_date": "2024-03-15",
    "due_date": "2024-04-15",
    "customer_name": "Tech Corp",
    "line_items": [
      {"description": "Widget A", "quantity": 100, "unit_price": 4.50, "amount": 450.00},
      {"description": "Shipping", "quantity": 1, "unit_price": 25.00, "amount": 25.00}
    ],
    "subtotal": 475.00,
    "tax_rate": "0%",
    "tax_amount": 0,
    "total": 475.00,
    "currency": "USD",
    "payment_terms": "Net 30"
  }
}
```

## Payment

- **Price**: $0.03 USDC per call
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
