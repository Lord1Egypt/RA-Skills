# rule-table.md (Mexico VAT/IVA)

> Data year: 2026 (compiled 2026-10). Items marked **[verify]** change or have tiered rates; confirm with SAT or a contador before relying.

## Rates
- Standard: 16%.
- Northern border zone: 8% (qualifying border municipalities) **[verify eligibility]**.
- Exports: 0% with proper documentation.

## Platform Withholding (since 2020-06-01)
- Digital platforms (Amazon MX, Mercado Libre) must withhold VAT and ISR (income tax) from sellers.
- Withholding tiers depend on: RFC provided or not; seller type (individual vs legal entity).
  - No RFC: maximum statutory withholding (historically up to full VAT + ~20% ISR) **[verify current rates]**.
  - RFC, individual: reduced withholding (historically ~50% of VAT + ~5.4% ISR) **[verify]**.
  - RFC, legal entity: generally self-declares (no ISR withholding) **[verify]**.
- The robust check: match the platform statement's withholding rate to the seller's RFC status — any mismatch is a finding.

## RFC Registration
- RFC = Registro Federal de Contribuyentes (SAT). Foreign sellers register via a legal representative in Mexico.
- No RFC + local stock: maximum withholding plus registration exposure.

## Import Rules
- De minimis: US$50 for most courier shipments (higher for USMCA-origin express) **[verify]**.
- Import IVA is creditable only when the seller is the importer of record on the pedimento.
- Using a courier's or platform's pedimento blocks the credit — a common hidden cost.

## CFDI E-Invoicing
- CFDI (current version 4.0) required for registered sellers **[verify version]**.
- B2B customers need valid CFDI to credit VAT — missing CFDI = credit disputes.

## Error Type & Cost Mapping (qualitative orientation estimates, not statistics)
| Error type | Frequency | Typical correction cost | Risk level |
|---|---|---|---|
| No RFC → maximum platform withholding | common | 8–20 points of gross margin | 🔴 |
| Withholding rate mismatched to RFC tier | common | US$500–US$3,000 | 🟡→🔴 |
| Import IVA credit claimed under wrong pedimento | occasional | credit denied + audit flag | 🟡 |
| Border-zone 8% misapplied | occasional | US$400–US$1,500 | 🟡 |
| Withholding not reconciled in monthly return | common | overpayment or deficiency | 🟡 |
| Missing CFDI on B2B sales | occasional | credit disputes | 🟡 |
