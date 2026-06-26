---
name: my-sg-invoice-parser
description: Extract structured data from Malaysian & Singaporean invoices/receipts. SST/GST-aware. Supports BM/EN/CN.
version: 2.0.0
metadata:
  openclaw:
    requires:
      env:
        - SKILLPAY_API_KEY
    emoji: "🧾"
    homepage: https://github.com/swmeng/myskills
---

# MY/SG Invoice & Receipt Parser

Extracts structured data from Malaysian and Singaporean invoices and receipts.

## How to Use This Skill

### Step 1: Charge billing and get tax rates

POST to the skill endpoint to authorize payment and retrieve current tax rates:

```
POST https://my-sg-invoice-parser.swmengappdev.workers.dev/parse
Content-Type: application/json

{
  "user_id": "<user_id>",
  "country": "MY"
}
```

The endpoint charges billing and returns current tax rates:
```json
{
  "success": true,
  "data": {
    "charged": true,
    "tax_rates": {
      "MY": {"service": 0.06, "sales": 0.10, "tourism": 0.08},
      "SG": {"gst": 0.09}
    }
  }
}
```

If payment fails, you'll receive a `payment_url` to share with the user.

### Step 2: Parse the invoice

Using your own capabilities, extract structured data from the invoice text or image. Support these languages:
- **Bahasa Malaysia** (BM)
- **English** (EN)
- **Chinese** (CN) - Simplified and Traditional

**For Malaysian invoices, detect:**
- SST Registration Number (look for "SST No" or "SST Reg")
- Service Tax: 6%
- Sales Tax: 10%
- Tourism Tax: 8%

**For Singaporean invoices, detect:**
- GST Registration Number (look for "GST Reg" or "GST No")
- GST: 9%

**Tax detection heuristics:**
- If text contains "SST" followed by "No" or "Reg" → Malaysian SST
- If text contains "GST" followed by "Reg" or "No" → Singapore GST
- Use the tax rates from Step 1 for calculations

### Step 3: Extract structured data

Extract the following fields:
- **vendor**: Business/company name
- **items**: Array of line items, each with:
  - `description`: Item name
  - `quantity`: Number of units
  - `unit_price`: Price per unit
  - `total`: Line total
- **subtotal**: Sum before tax
- **tax_type**: "MY_SST_service", "MY_SST_sales", "SG_GST", etc.
- **tax_amount**: Calculated tax amount
- **total**: Final total including tax
- **currency**: "MYR" for Malaysia, "SGD" for Singapore

### Output Format

Return the parsed invoice as JSON:

```json
{
  "vendor": "Restoran Nasi Kandar Line Clear",
  "items": [
    {"description": "Nasi Campur", "quantity": 2, "unit_price": 12.50, "total": 25.00},
    {"description": "Teh Tarik", "quantity": 2, "unit_price": 3.50, "total": 7.00}
  ],
  "subtotal": 32.00,
  "tax_type": "MY_SST_service",
  "tax_amount": 1.92,
  "total": 33.92,
  "currency": "MYR"
}
```

## Pricing
$0.02 USDT per call via SkillPay.me
