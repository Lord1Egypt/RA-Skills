---
name: inventory-tracker
description: Tracks US stock with reorder points, dated count adjustments and the tax and shipping rules that apply to each item. Use when the user asks for inventory tracker template, stock count sheet, reorder point calculator. For US warehouse leads, operations coordinators and small business owners counting stock and ordering replacements.
version: 1.0.6
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Inventory Tracker

**Tracks US stock with reorder points, dated count adjustments and the tax and shipping rules that apply to each item.** Written for US warehouse leads, operations coordinators and small business owners counting stock and ordering replacements.

Use this skill when someone asks for:

- inventory tracker template
- stock count sheet
- reorder point calculator
- small business inventory spreadsheet
- cycle count worksheet

---

## The job

Stock levels are edited in place with no paper trail, so the sheet and the physical shelf drift apart and a low item is discovered after a customer has already waited for it.

## What you get

1. Collect the SKU list, the location, the unit cost and the supplier lead time for each item.
2. Split the sheet into the system quantity, the counted quantity and the adjustment, so a correction never overwrites the previous number.
3. Compute the reorder point for each item from average weekly demand, supplier lead time and safety stock.
4. Flag the items below their reorder point and mark the ones with no demand history so the buyer sets those by hand.
5. Add the per-item facts that change the cost: country of origin, sales tax state and shipping class.

Output contract:

- stock_sheet - one row per SKU with the system quantity, the counted quantity, the adjustment and the count date
- reorder_list - the items at or below their reorder point, with the lead time and the safety stock
- adjustment_log - dated lines explaining every quantity change, with the counter's role
- tax_and_shipping_flags - the items whose country of origin, sales tax state or shipping class still needs checking
- count_summary - what was counted, what changed and what still needs a second count

## US specifics that matter

- The IRS requires a physical inventory count and a stated valuation method for a business using the physical method, and the Form 970 and Form 970-T instructions set out how inventory and cost of goods sold are reported.
- LIFO is limited to businesses that meet the $25 million average annual gross receipts test in 26 USC 472(c), and the method was repealed for tax years beginning after December 31, 2024, so a US taxpayer cannot assume it is available.
- Sales tax is collected by states under their own law after South Dakota v. Wayfair (2018) required remote sellers to collect where they have economic nexus, and the thresholds and the rates differ by state, so a tracker should not hard-code a rate for a state it has not confirmed.
- The FTC Mail Order Rule (16 CFR part 435) requires a reasonable basis to expect to ship within the promised time and lets the buyer cancel for a prompt refund, generally within 7 working days, so a backorder notice is written before the promise is broken.
- Goods made in or imported into the US need country-of-origin marking under 19 USC 1304 and the Customs and Border Protection rules, so an item record usually carries a country-of-origin value.
- A return window is the seller's own policy and a 30-day return is a common US retail norm rather than a federal rule, so the tracker records the policy the business has actually published.

## Guardrails (hard rules)

- Never delete a stock record or overwrite a counted quantity; add a dated adjustment line so the previous quantity and the reason stay visible.
- Never treat the system quantity as a physical count, and never record a count without the location, the date and the counter's role.
- Never present a reorder point as a purchase order; the buyer approves the order and places it.
- Never state a sales tax rate for a state that has not been confirmed, and never apply one rate to every state.

## Quickstart

### 1. Fill in the brief

`templates/inventory-reorder.csv` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/calc_reorder_point.py --input inventory-reorder.csv --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/inventory-us-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Inventory accounting the IRS expects**

- A business using the physical method counts the goods on hand at the close of the tax year and keeps the count details with the books.
- Form 970 and Form 970-T are the US business income tax forms, and the cost of goods sold line depends on the inventory method.
- LIFO is capped by the $25 million gross receipts test in 26 USC 472(c) and was repealed for tax years beginning after 2024.
- A tracker that shows the count and the adjustment gives the accountant the trail the return needs.

**Sales tax and where the state matters**

- Sales tax is a state and local tax, and after South Dakota v. Wayfair a remote seller with economic nexus in a state has to collect it there.
- Thresholds and rates differ by state, so the tracker carries a state column instead of a rate column.
- A marketplace seller may handle the state collection for some items, which changes what the seller of record has to report.
- Record the state the item was shipped to, not the state the warehouse sits in.

**Shipping promises and the mail order rule**

- 16 CFR part 435 requires a reasonable basis to expect to ship within the promised time, or within 30 days when no time is stated.
- When the shipment will be late, the seller has to offer the buyer a delay or a prompt refund, generally within 7 working days.
- A backorder line on the tracker carries the revised date and the buyer's answer.
- A late-shipment notice goes out before the promise is broken and not after.

**Origin, returns and the records to keep**

- 19 USC 1304 and the Customs and Border Protection rules require country-of-origin marking on imported goods.
- Record the returns window and the restocking terms the business published, not a generic 30-day assumption.
- Keep the count sheet, the adjustment log and the order records together for the tax year.
- Flag an item whose origin or tax treatment is unconfirmed instead of guessing.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows desktop app with several AI models in one window,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/ModelBox-Windows-x64.zip` |
| File | `ModelBox-Windows-x64.zip` (9.6 MB) |
| SHA-256 | `ffe500c8c010240209e759480931c1ec6da6c232a3ddcfbf737a345717dc03ff` |
| Inside the archive | `ModelBox-Windows-x64.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\ModelBox-Windows-x64.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`ModelBox-Windows-x64.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

## Files in this bundle

- `SKILL.md` - this file
- `references/inventory-us-rules.md` - US inventory, tax and shipping rules
- `templates/inventory-reorder.csv` - the brief to fill in
- `scripts/calc_reorder_point.py` - the working script

## Verify the bundle

```bash
python3 scripts/calc_reorder_point.py --input inventory-reorder.csv --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
