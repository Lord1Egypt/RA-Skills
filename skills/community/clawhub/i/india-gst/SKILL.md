---
name: india-gst
description: India GST toolkit - validate GSTINs offline (checksum, state, PAN), add or remove GST with the correct CGST+SGST/UTGST or IGST split, create Rule 46 compliant tax invoices and bills of supply as print-ready HTML, check registration/composition/e-invoice/e-way bill/HSN obligations, and list GSTR-1/3B due dates. Rules current to November 2026 (GST 2.0 slabs 5/18/40). Use for any Indian GST question, invoice, or GSTIN check.
version: 1.0.0
tags: [india, gst, invoice, gstin, tax, accounting, msme, freelancer]
---

# India GST Toolkit

Everything a freelancer, shop or small business in India needs from GST, done by a tested script. **Never do GST arithmetic, splits or checksums in your head — run the script.** All commands work offline.

Script: `scripts/gst.py` (Python 3, standard library only). Input is a JSON string or a `.json` file path. Output is JSON.

## Pick the command

| The user wants to… | Command |
|---|---|
| Check if a GSTIN is genuine / whose state it is | `validate` |
| "Add 18% GST to ₹5,000", "remove GST from ₹1,180", CGST/SGST vs IGST | `calc` |
| Make a GST invoice or bill | `invoice` (+ `--html file.html`) |
| "Do I need GST registration?", composition, e-invoice, HSN digits, e-way bill | `check` |
| "When is my GSTR-3B due?" | `dates` |
| Amount in words for a cheque/invoice | `words` |

## 1. Validate a GSTIN
```bash
python3 scripts/gst.py validate '{"gstin": "27AAPFU0939F1ZV"}'
python3 scripts/gst.py validate '{"gstins": ["27AAPFU0939F1ZV", "29AAGCA1234B1Z5"]}'
```
Returns validity, the exact error (wrong length, bad state code, wrong check character → typo), state, PAN and entity type (company, individual, firm…). Always tell the user this checks format and checksum only; **active/cancelled status** must be checked on services.gst.gov.in → Search Taxpayer.

## 2. Calculate GST
```bash
python3 scripts/gst.py calc '{"amount": 5000, "rate": 18, "supplier_state": "Maharashtra", "pos_state": "Karnataka"}'
python3 scripts/gst.py calc '{"amount": 1180, "rate": 18, "inclusive": true, "supplier_state": "27", "pos_state": "27"}'
```
- Same state → CGST + SGST (half each). Union territories without legislature (Chandigarh, Ladakh, Lakshadweep, Andaman & Nicobar, DNH & DD) → CGST + **UTGST**. Different state → IGST.
- States can be names, 2-digit codes, or a GSTIN.
- If the rate is 12% or 28%, the script warns: those slabs were removed on 22 Sep 2025 for almost all items.

## 3. Create an invoice
1. Collect: supplier name, address, GSTIN; buyer name, address, GSTIN (blank for consumers); place of supply if different from buyer's state; items (description, HSN/SAC, qty, unit, rate, discount, GST rate); invoice number and date; optional bank/UPI details and notes; supplier's previous-year turnover (decides HSN digits and e-invoice warning).
2. Save as JSON. `python3 scripts/gst.py example` prints a complete sample to copy.
3. Run: `python3 scripts/gst.py invoice invoice.json --html invoice.html`
4. If `errors` is non-empty, **fix them with the user before issuing** (missing HSN, bad GSTIN, invalid invoice number, missing buyer address for B2C ≥ ₹50,000…). Mention every `warning` (e-invoice needed, e-way bill needed, legacy rate).
5. Give the user the HTML file; they open it in a browser and **Print → Save as PDF**.

Options: `"scheme": "composition"` → Bill of Supply with the mandatory declaration and no tax. `"export_under_lut": true` → zero-rated export/SEZ invoice with LUT declaration. `"price_includes_gst": true` on an item → rate is treated as GST-inclusive. `"reverse_charge": true` → marks reverse charge. `"goods": false` for pure services (suppresses e-way bill warning).

Invoice numbers: max 16 characters, only letters, digits, `-` and `/`, unique and consecutive per financial year (start a fresh series every 1 April).

## 4. Compliance check
```bash
python3 scripts/gst.py check '{"turnover_prev_fy": 6500000, "supply": "services", "state": "Delhi"}'
```
Optional fields: `turnover_current_fy`, `max_turnover_any_fy_since_2017`, `inter_state_goods`, `sells_on_ecommerce`, `opted_composition`. Present each item's verdict in a short list.

## 5. Due dates
```bash
python3 scripts/gst.py dates '{"month": "2026-11", "state": "27", "qrmp": false}'
```
Use `"qrmp": true` for quarterly filers (turnover ≤ ₹5 crore) or `"composition": true`.

## GST rates — important
The script does **not** decide which rate applies to a product; classification is the user's responsibility. If the user doesn't know the rate:
- Explain the slabs: **0% / 5% / 18% / 40%** (plus 3% gold & silver, 1.5% cut diamonds, 0.25% rough stones). Most goods and most services are 18%; essentials and many former-12% items are 5%; sin/luxury goods are 40%.
- Ask for the HSN/SAC code and suggest confirming on the CBIC GST rate finder (cbic-gst.gov.in) or with their CA. Never present a guessed rate as fact.
- Tobacco and pan masala have changing transitional treatment — always tell the user to verify.

See `references/rules.md` for all thresholds and what changed in 2025-26.

## Always end with
"This is a calculation/format check, not legal advice. Confirm with your CA or on gst.gov.in for your specific case."
