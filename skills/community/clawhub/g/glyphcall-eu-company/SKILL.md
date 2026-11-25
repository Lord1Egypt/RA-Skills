---
name: eu-company-check
description: |
  Know-your-business and e-invoice checks for EU counterparties in one call: official company
  registers, VAT (VIES) validation, sanctions screening and invoice format rules.

  USE FOR:
  - Verifying that an EU company exists and its VAT number is valid before paying an invoice
  - Screening a company or address against sanctions lists
  - Checking whether an XRechnung or ZUGFeRD e-invoice will be accepted

  TRIGGERS:
  - "verify this company", "KYB", "VAT number check", "VIES validation"
  - "sanctions screening", "is this counterparty sanctioned"
  - "XRechnung validator", "ZUGFeRD check", "e-invoice valid"
  Sold as x402/MPP pay-per-call tools on Base and Solana; agents pay per successful call.
metadata:
  version: 1
---

# EU company check

| Task | Endpoint | Price |
|------|----------|-------|
| KYB bundle | `https://api.glyphcall.com/pack/kyb-eu?...` | $0.02 |
| VAT validation | `https://api.glyphcall.com/vat/validate?vat=<number>` | $0.01 |
| E-invoice check | `https://api.glyphcall.com/pack/einvoice-check?...` | $0.01 |
| Sanctions screen | `https://api.glyphcall.com/sanctions/check?name=<name>` | $0.01 |

```sh
npx agentcash@latest check "https://api.glyphcall.com/vat/validate?vat=DE123456789"
npx agentcash@latest fetch "https://api.glyphcall.com/vat/validate?vat=DE123456789"
```

Always check the parameter names with `agentcash check` first; a failed validation is not charged.
Results come from official registers and VIES where available, with the source recorded.

