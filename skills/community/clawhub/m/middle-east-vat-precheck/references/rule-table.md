# rule-table.md (Middle East VAT)

> Data year: 2026 (compiled 2026-10). Items marked **[verify]** are recent or phased; confirm with FTA (UAE) / ZATCA (KSA) before relying.

## Rates
- UAE: 5% (since 2018-01-01).
- Saudi Arabia: 15% (since 2020-07-01, raised from 5%).
- Expansion notes: Bahrain 10% (since 2022), Oman 5% (since 2021); Kuwait/Qatar not yet implemented VAT **[verify status]**.

## Registration
- Residents: mandatory registration threshold AED 375,000 / SAR 375,000 annual taxable supplies (voluntary from 50% of that).
- **Non-residents making taxable supplies: NO threshold — registration required from the first supply.**
- KSA: non-residents must appoint a local tax representative.
- Reverse charge may apply to B2B supplies to VAT-registered recipients — flag misapplied reverse charge on B2C.

## Platform & Stock
- Amazon.ae / Noon: NO deemed-supplier regime — platforms do not collect VAT for goods sellers.
- FBA / local warehouse stock = domestic supplies, registration required.
- Cross-border direct B2C: import VAT at customs; clarify DDP (seller-borne) vs DDU (buyer-borne) to avoid disputes.

## Invoicing & E-Invoicing
- Tax invoices required in Arabic or bilingual (Arabic + English).
- KSA e-invoicing (Fatoora): Phase 2 integration applies to VAT-registered persons in turnover-based waves **[verify current wave & applicability]**.
- UAE: FTA tax invoice mandatory fields; simplified invoices allowed for B2C under thresholds.

## Error Type & Cost Mapping (qualitative orientation estimates, not statistics)
| Error type | Frequency | Typical correction cost | Risk level |
|---|---|---|---|
| Non-resident assuming AED/SAR 375k threshold applies | common | back taxes from first sale + penalties | 🔴 |
| UAE 5% rate applied to KSA (15%) or vice versa | common | US$800–US$3,000 | 🟡→🔴 |
| FBA stock without local registration | common | account suspension + back taxes | 🔴 |
| No KSA tax representative appointed | occasional | registration blocked/revoked | 🔴 |
| Missing Arabic tax invoice fields | occasional | B2B credit disputes | 🟡 |
| DDP/DDU confusion on direct shipping | occasional | US$300–US$1,500 | 🟡 |

## Risk Reference
- 🔴 correction cost > US$2,000 or account/registration exposure · 🟡 US$500–2,000 · 🟢 below
