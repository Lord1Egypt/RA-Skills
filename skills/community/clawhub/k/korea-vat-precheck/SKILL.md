---
name: korea-vat-precheck
display_name: Korea VAT Pre-Check
description: "Korea VAT pre-check for cross-border sellers (Coupang, Naver SmartStore, Gmarket). Upload draft filing data and platform statements to check six high-frequency error categories: rate application, de minimis & personal clearance, local stock registration, platform collection boundary, filing frequency, pricing & cash receipts — outputs a structured risk report. Trigger words: Korea VAT pre-check, Korea tax check, Coupang seller tax, PCCC."
category: productivity
version: 0.1.0
author: snow
allowed-tools: ""
---

# Korea VAT Pre-Check

## Red Lines
- Pre-check only, never filing. Passing the pre-check ≠ compliance.
- Never generate official returns or registration documents.
- When information is insufficient, state "cannot determine" — do not guess. Items marked "verify" in references must not be asserted without user-provided confirmation.
- Do not request API keys, passwords, or network access.

## Step 1 — Information Collection
Collect in one pass: 1) sales channels (Coupang / Naver SmartStore / Gmarket / own site); 2) annual Korea sales; 3) whether holding a Korean business registration; 4) typical order value (vs the US$150 de minimis); 5) fulfillment model (cross-border direct vs Coupang Rocket/local 3PL stock); 6) customer type (B2C / includes B2B / unsure); 7) whether buyers' personal customs clearance codes (PCCC) are collected for direct shipments. If information is incomplete, pre-check with what is available and mark the missing items.

## Step 2 — Item-by-Item Pre-Check
Check against `references/rule-table.md` and `references/deadlines.md`:
A. Rate: flat 10% — the simple part; flag zero-rating/export confusion on goods shipped INTO Korea.
B. De minimis & PCCC: ≤ US$150 (US$200 for US-origin) duty/VAT-exempt for personal-use imports with the buyer's PCCC — flag bulk commercial shipments split into PCCC personal entries (seizure + back-tax risk, 🔴).
C. Local stock registration: inventory in Coupang Rocket or local 3PL = domestic sales → Korean business registration and VAT filing required — flag selling from local stock unregistered.
D. Platform collection boundary: Korea has NO marketplace deemed-supplier regime for goods — Coupang/Naver do not remit VAT for the seller; the e-service VAT regime (since 2015) covers foreign DIGITAL service providers only, not goods.
E. Frequency & deadlines: individuals file quarterly (due the 25th after quarter end); corporations semiannually (due the 25th after the half-year); preliminary return periods exist for corporations — flag missed preliminary filings.
F. Pricing & receipts: consumer prices VAT-inclusive; registered sellers must issue cash receipts or tax invoices on request — flag missing issuance on B2B requests.

## Step 3 — Report
Part 1 — Risk summary: 🔴 high risk / 🟡 needs attention / 🟢 no obvious high-frequency errors found (not a compliance conclusion).
Part 2 — Table: check item | finding | risk level | basis | recommended action. 🔴 = estimated correction cost >US$2,000 or customs/registration exposure; 🟡 = US$500–2,000; 🟢 = no anomaly found (not a compliance conclusion).
Part 3 — Next steps: 1–3 prioritized actions; where registration or back-filing is involved, note "confirm with a Korean tax advisor (세무사)."

## Step 4 — Follow-Ups
Expand only on already-checked items. If asked to file returns or register, reply: "This skill performs pre-checks only and does not file or register. Please hand the report to your 세무사."

---
Series: cross-border tax pre-check (EU `eu-vat-precheck-en` · US `us-sales-tax-precheck` · Japan `japan-jct-precheck` · Australia `australia-gst-precheck` · SEA `southeast-asia-vat-precheck` · Canada `canada-gst-hst-precheck` · Middle East `middle-east-vat-precheck` · Mexico `mexico-vat-precheck` · Korea `korea-vat-precheck`).
