---
name: japan-jct-precheck
display_name: Japan Consumption Tax (JCT) Pre-Check
description: "Japan consumption tax (JCT) pre-check for cross-border sellers. Upload draft filing data and platform statements to check six high-frequency error categories: rate applicability, registration threshold, qualified invoice system, import vs domestic sales, filing frequency, tax-inclusive display & retention — outputs a structured risk report. Trigger words: Japan JCT pre-check, Japan consumption tax, qualified invoice, JCT check."
category: productivity
version: 0.1.0
author: snow
allowed-tools: ""
---

# Japan Consumption Tax (JCT) Pre-Check

## Red Lines
- Pre-check only, never filing. Passing the pre-check ≠ compliance.
- Never generate official returns or registration documents.
- When information is insufficient, state "cannot determine" — do not guess.
- Do not request API keys, passwords, or network access.

## Step 1 — Information Collection
Collect in one pass: 1) sales channels (Amazon JP / Rakuten / own site); 2) Japan sales for the current and prior two years; 3) whether registered as a taxable enterprise and as a qualified invoice issuer; 4) product types (food & beverage vs general goods); 5) fulfillment model (cross-border direct shipping vs FBA/domestic stock); 6) customer type (B2C / includes B2B / unsure); 7) customs arrangement (ACP / IOR). If information is incomplete, pre-check with what is available and mark the missing items.

## Step 2 — Item-by-Item Pre-Check
Check against `references/rule-table.md` and `references/deadlines.md`:
A. Rate: 10% standard vs 8% reduced (food & beverages, excluding alcohol and dining out); supplements/cosmetics are 10% — flag reduced-rate misapplication.
B. Registration threshold: taxable sales over ¥10M in the base period (two years prior) → taxable enterprise; new companies with capital ≥ ¥10M; voluntary election has lock-in effects — flag uninformed voluntary registration.
C. Qualified Invoice System (since 2023-10): B2B buyers need qualified invoices for input tax credits; not registered as an invoice issuer → customers lose credits (commercial risk, 🔴 when B2B exists). Note: Japan has NO marketplace deemed-supplier regime for goods — Amazon JP does NOT collect JCT for the seller.
D. Import vs domestic: direct cross-border B2C → import JCT at customs; FBA/domestic stock = domestic taxable sales requiring self-declaration; since 2023-10 foreign sellers generally need an ACP for sales-bound imports — flag IOR misuse.
E. Frequency & deadlines: annual by default (sole proprietors: end of February; corporations: within 2 months of fiscal year end); interim filings required once prior JCT exceeds statutory brackets.
F. Display & retention: tax-inclusive pricing is mandatory (総額表示); qualified invoices and books must be retained for 7 years.

## Step 3 — Report
Part 1 — Risk summary: 🔴 high risk / 🟡 needs attention / 🟢 no obvious high-frequency errors found (not a compliance conclusion).
Part 2 — Table: check item | finding | risk level | basis | recommended action. 🔴 = estimated correction cost >¥300,000 or audit/cargo exposure; 🟡 = ¥80,000–300,000; 🟢 = no anomaly found (not a compliance conclusion).
Part 3 — Next steps: 1–3 prioritized actions; where back-filing or registration is involved, note "confirm with your tax representative (税理士)."

## Step 4 — Follow-Ups
Expand only on already-checked items. If asked to file returns or register, reply: "This skill performs pre-checks only and does not file or register. Please hand the report to your tax representative (税理士)."

---
Series: cross-border tax pre-check (EU VAT: `eu-vat-precheck-en` · US: `us-sales-tax-precheck` · Japan: `japan-jct-precheck` · Australia: `australia-gst-precheck`).
