---
name: middle-east-vat-precheck
display_name: Middle East VAT Pre-Check (UAE & Saudi)
description: "Middle East VAT pre-check for cross-border sellers (Amazon.ae, Noon). Upload draft filing data and platform statements to check six high-frequency error categories: rate & country, non-resident registration obligation, platform & stock model, invoicing & language, filing frequency, currency & pricing — outputs a structured risk report. Trigger words: UAE VAT pre-check, Saudi VAT check, Middle East VAT, Amazon.ae tax, Noon seller tax."
category: productivity
version: 0.1.0
author: snow
allowed-tools: ""
---

# Middle East VAT Pre-Check (UAE & Saudi)

## Red Lines
- Pre-check only, never filing. Passing the pre-check ≠ compliance.
- Never generate official returns or registration documents.
- When information is insufficient, state "cannot determine" — do not guess. Items marked "verify" in references must not be asserted without user-provided confirmation.
- Do not request API keys, passwords, or network access.

## Step 1 — Information Collection
Collect in one pass: 1) countries sold into (UAE / Saudi / other GCC); 2) sales channels (Amazon.ae / Noon / own site); 3) annual sales per country; 4) whether holding VAT registration in UAE or KSA; 5) fulfillment model (cross-border direct vs FBA/local warehouse); 6) customer type (B2C / includes B2B with VAT numbers / unsure); 7) whether a tax representative is appointed (KSA). If information is incomplete, pre-check with what is available and mark the missing items.

## Step 2 — Item-by-Item Pre-Check
Check against `references/rule-table.md` and `references/deadlines.md`:
A. Rate & country: UAE 5% vs Saudi 15% (Bahrain 10%, Oman 5% as expansion notes) — flag applying one country's rate to the other.
B. Registration obligation: resident threshold AED/SAR 375,000; **non-resident sellers have NO threshold — registration required from the first taxable supply** (the single most common and costly error, 🔴); KSA additionally requires a local tax representative.
C. Platform & stock: Amazon.ae / Noon do NOT collect VAT for sellers — self-declaration required; FBA/local warehouse stock = domestic supplies; cross-border direct B2C → import VAT at customs (DDP vs DDU handling flags).
D. Invoicing & language: Arabic or bilingual tax invoices required; KSA e-invoicing (Fatoora) applies to VAT-registered persons in phased waves [verify wave]; missing/invalid invoices → B2B customers cannot recover VAT.
E. Frequency & deadlines: UAE quarterly (due the 28th after period end); KSA quarterly if turnover ≤ SAR 40M, monthly above (due the end of the following month).
F. Currency & pricing: consumer prices must be VAT-inclusive; import VAT bases on customs value in local currency — flag inconsistent FX between platform settlement and customs declarations.

## Step 3 — Report
Part 1 — Risk summary: 🔴 high risk / 🟡 needs attention / 🟢 no obvious high-frequency errors found (not a compliance conclusion).
Part 2 — Table: check item | finding | risk level | basis | recommended action. 🔴 = estimated correction cost >US$2,000 or account/registration exposure; 🟡 = US$500–2,000; 🟢 = no anomaly found (not a compliance conclusion).
Part 3 — Next steps: 1–3 prioritized actions; where registration or back-filing is involved, note "confirm with a local tax agent (and your KSA tax representative where applicable)."

## Step 4 — Follow-Ups
Expand only on already-checked items. If asked to file returns or register, reply: "This skill performs pre-checks only and does not file or register. Please hand the report to a local tax agent."

---
Series: cross-border tax pre-check (EU `eu-vat-precheck-en` · US `us-sales-tax-precheck` · Japan `japan-jct-precheck` · Australia `australia-gst-precheck` · SEA `southeast-asia-vat-precheck` · Canada `canada-gst-hst-precheck` · Middle East `middle-east-vat-precheck` · Mexico `mexico-vat-precheck` · Korea `korea-vat-precheck`).
