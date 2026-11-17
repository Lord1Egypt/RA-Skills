---
name: mexico-vat-precheck
display_name: Mexico VAT Pre-Check
description: "Mexico VAT (IVA) pre-check for cross-border sellers (Amazon MX, Mercado Libre). Upload draft filing data and platform statements to check six high-frequency error categories: rate & zone, RFC registration, platform withholding tiers, import & pedimento handling, filing frequency, pricing & CFDI e-invoicing — outputs a structured risk report. Trigger words: Mexico VAT pre-check, Mexico IVA check, RFC withholding, Mercado Libre tax, Amazon Mexico tax."
category: productivity
version: 0.1.0
author: snow
allowed-tools: ""
---

# Mexico VAT (IVA) Pre-Check

## Red Lines
- Pre-check only, never filing. Passing the pre-check ≠ compliance.
- Never generate official returns or registration documents.
- When information is insufficient, state "cannot determine" — do not guess. Items marked "verify" in references must not be asserted without user-provided confirmation.
- Do not request API keys, passwords, or network access.

## Step 1 — Information Collection
Collect in one pass: 1) sales channels (Amazon MX / Mercado Libre / own site); 2) annual Mexico sales; 3) whether holding an RFC tax registration (and seller type: individual vs legal entity); 4) current withholding rates shown on platform statements; 5) fulfillment model (cross-border direct vs FBA/local warehouse); 6) imports handled under whose pedimento (customs entry); 7) product types. If information is incomplete, pre-check with what is available and mark the missing items.

## Step 2 — Item-by-Item Pre-Check
Check against `references/rule-table.md` and `references/deadlines.md`:
A. Rate & zone: standard 16%; northern border zone 8% — flag applying border-zone rates to non-qualifying regions.
B. RFC registration: no RFC → platforms withhold at maximum statutory rates (the single biggest margin leak, 🔴); foreign sellers register via a legal representative — flag operating local stock without RFC.
C. Platform withholding tiers (since 2020-06): withholding depends on RFC status and seller type (individual vs entity) — verify the rates on the platform statement match the seller's tier [verify current rates]; withheld VAT/ISR must be reconciled against the final liability.
D. Import & pedimento: import IVA paid at customs is creditable only if the seller is the importer of record on the pedimento — flag claiming credits under a courier's/platform's pedimento; de minimis US$50 for most shipments [verify].
E. Frequency & deadlines: monthly returns, due the 17th of the following month; reconcile platform withholding statements against filed returns.
F. Pricing & CFDI: consumer prices VAT-inclusive; CFDI 4.0 e-invoicing required for registered sellers [verify version]; missing/invalid CFDI → B2B customers cannot credit.

## Step 3 — Report
Part 1 — Risk summary: 🔴 high risk / 🟡 needs attention / 🟢 no obvious high-frequency errors found (not a compliance conclusion).
Part 2 — Table: check item | finding | risk level | basis | recommended action. 🔴 = estimated correction cost >US$2,000 or account/withholding exposure; 🟡 = US$500–2,000; 🟢 = no anomaly found (not a compliance conclusion).
Part 3 — Next steps: 1–3 prioritized actions; where registration or back-filing is involved, note "confirm with a Mexican tax advisor (contador)."

## Step 4 — Follow-Ups
Expand only on already-checked items. If asked to file returns or register, reply: "This skill performs pre-checks only and does not file or register. Please hand the report to your contador."

---
Series: cross-border tax pre-check (EU `eu-vat-precheck-en` · US `us-sales-tax-precheck` · Japan `japan-jct-precheck` · Australia `australia-gst-precheck` · SEA `southeast-asia-vat-precheck` · Canada `canada-gst-hst-precheck` · Middle East `middle-east-vat-precheck` · Mexico `mexico-vat-precheck` · Korea `korea-vat-precheck`).
