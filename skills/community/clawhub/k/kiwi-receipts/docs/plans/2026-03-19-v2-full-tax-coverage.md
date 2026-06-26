# Kiwi Receipts v2.0 — Full NZ Tax Coverage

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Extend kiwi-receipts from GST-only to cover sales/income tracking, IR3 annual income tax, provisional tax, asset depreciation, and Xero CSV export — turning it into a near-complete personal tax assistant for NZ sole trader builders.

**Architecture:** Add 3 new JSON data files (income.json, assets.json, tax-history.json) alongside existing receipts.json. Extend config.json with new fields. Add new reference docs for income tax, depreciation, and provisional tax. Extend generate_report.py with new sheet generators. Update SKILL.md with new commands and compliance rules.

**Tech Stack:** Python 3 (openpyxl for XLSX, csv module for Xero export), JSON flat-file storage, OpenClaw SKILL.md format.

---

## Task 1: New Reference — NZ Income Tax Guide

**Files:**
- Create: `references/nz-income-tax-guide.md`

**Step 1: Create the income tax reference file**

```markdown
# NZ Income Tax Reference for Sole Traders

> **Authoritative sources:**
> - [Income Tax Act 2007 (NZ)](https://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1512301.html)
> - [IRD — Tax rates for individuals](https://www.ird.govt.nz/income-tax/income-tax-for-individuals/tax-codes-and-tax-rates-for-individuals/tax-rates-for-individuals)
> - [IRD — Individual income tax return IR3](https://www.ird.govt.nz/income-tax/income-tax-for-individuals/what-happens-at-the-end-of-the-tax-year/individual-income-tax-return---ir3)
> - [IRD — Provisional tax standard option](https://www.ird.govt.nz/income-tax/provisional-tax/provisional-tax-options/standard-option)

---

## 1. Income Tax Rates (from 1 April 2025)

Income Tax Act 2007, Schedule 1, Part A:

| Taxable Income | Rate |
|----------------|------|
| $0 - $15,600 | 10.5% |
| $15,601 - $53,500 | 17.5% |
| $53,501 - $78,100 | 30% |
| $78,101 - $180,000 | 33% |
| $180,001 and over | 39% |

These are **progressive** rates — each bracket only applies to income within that range.

### Tax calculation example (taxable income $90,000):

| Bracket | Income in bracket | Rate | Tax |
|---------|-------------------|------|-----|
| $0 - $15,600 | $15,600 | 10.5% | $1,638.00 |
| $15,601 - $53,500 | $37,900 | 17.5% | $6,632.50 |
| $53,501 - $78,100 | $24,600 | 30% | $7,380.00 |
| $78,101 - $90,000 | $11,900 | 33% | $3,927.00 |
| **Total** | | | **$19,577.50** |

### ACC Earner's Levy (2025/2026)

- Rate: **1.67%** of gross earnings
- Maximum insurable earnings: **$152,790**
- Maximum levy: $152,790 x 1.67% = **$2,551.59**

This is deducted automatically from PAYE but must be calculated separately for sole traders.

---

## 2. IR3 Return Structure

The IR3 is filed once per year for the tax year ending 31 March.

### Key sections for a sole trader builder:

**Section: Income**
- Gross business income (total sales/invoices for the year)
- Schedular payments received (if any)
- Interest income
- Other income

**Section: IR3B — Schedule of Business Income**
- Gross income from self-employment
- Opening stock/inventory
- Purchases
- Closing stock/inventory
- Gross profit
- Expenses by category:
  - Accounting fees
  - Advertising
  - Bad debts
  - Depreciation
  - Fuel/vehicle expenses
  - Insurance
  - Interest on business loans
  - Materials/supplies
  - Rent
  - Repairs and maintenance
  - Subcontractor payments
  - Telephone/internet
  - Tools
  - Travel
  - Other
- Net profit (= gross profit - total expenses)

**Section: Tax Calculation**
- Taxable income = net profit + other income
- Tax on taxable income (using bracket table)
- Less: tax already paid (PAYE, RWT, provisional tax)
- = Tax to pay or refund due

### Filing deadlines:

| Scenario | Due date |
|----------|----------|
| Self-filing | 7 July (same calendar year) |
| Via tax agent | 31 March (following calendar year) |

---

## 3. Provisional Tax — Standard Method

**Income Tax Act 2007, Part RC:**

### Who must pay:

Residual income tax (RIT) exceeds **$5,000** in the previous year.

### Calculation:

```
Provisional tax = previous year's RIT x 105%
Each instalment = total / 3
```

If previous year return not yet filed, use RIT from 2 years ago x 110%.

### Payment dates (March balance date):

| Instalment | Due date |
|------------|----------|
| 1st | 28 August |
| 2nd | 15 January |
| 3rd | 7 May |

### Example:

Previous year tax: $15,670
Provisional tax: $15,670 x 1.05 = $16,453.50
Per instalment: $16,453.50 / 3 = $5,484.50

---

## 4. Deductible Business Expenses

Income Tax Act 2007, Section DA 1 — General permission:
> A person is allowed a deduction for an amount to the extent that it is incurred in deriving assessable income or in carrying on a business.

### Common sole trader builder deductions:

| Category | Description | Notes |
|----------|-------------|-------|
| Materials | Timber, concrete, paint, fixings | Fully deductible |
| Tools | Power tools, hand tools | Depreciate if > $500 |
| Fuel | Petrol/diesel for work vehicle | Business % only |
| Vehicle | WOF, tyres, repairs, rego, insurance | Business % only |
| Safety | PPE, hi-vis, hard hats, boots | Fully deductible |
| Subcontractors | Payments to other tradies | Fully deductible |
| Insurance | Public liability, tools insurance | Fully deductible |
| Phone/internet | Mobile, broadband | Business % only |
| Depreciation | Vehicles, tools, equipment | See depreciation guide |
| Home office | If working from home | Floor area % method |
| ACC levies | Work levy portion | Fully deductible |
| Accounting fees | Accountant costs | Fully deductible |

### Non-deductible:
- Personal expenses
- Entertainment (50% only for meals with clients)
- Fines and penalties
- Capital expenditure (must depreciate instead)

---

## 5. Important Dates — Annual Calendar

| Date | What |
|------|------|
| 31 March | End of tax year |
| 7 May | GST return due (Feb-Mar period) + 3rd provisional tax instalment |
| 7 July | IR3 due (self-filing) |
| 28 August | 1st provisional tax instalment |
| 15 January | 2nd provisional tax instalment + GST return due (Nov-Dec period) |
| 31 March | IR3 due (via tax agent, following year) |

---

*Last updated: March 2026. Based on Income Tax Act 2007 and Tax Administration Act 1994 as current. Always verify rates at [ird.govt.nz](https://www.ird.govt.nz).*
```

**Step 2: Commit**

```bash
git add references/nz-income-tax-guide.md
git commit -m "docs: add NZ income tax reference for sole traders"
```

---

## Task 2: New Reference — NZ Depreciation Rates

**Files:**
- Create: `references/nz-depreciation-rates.md`

**Step 1: Create the depreciation reference file**

```markdown
# NZ Depreciation Rates for Construction Assets

> **Authoritative sources:**
> - [Income Tax Act 2007, Subpart EE — Depreciation](https://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1514842.html)
> - [IRD — General depreciation rates IR265 (August 2024)](https://www.ird.govt.nz/-/media/project/ir/home/documents/forms-and-guides/ir200---ir299/ir265/ir265-august-2024.pdf)
> - [IRD — Depreciation rate finder](https://www.ird.govt.nz/income-tax/income-tax-for-businesses-and-organisations/types-of-business-expenses/depreciation/claiming-depreciation/work-out-your-assets-rate-and-depreciation-value)
> - [IRD — Claiming depreciation](https://www.ird.govt.nz/income-tax/income-tax-for-businesses-and-organisations/types-of-business-expenses/depreciation/claiming-depreciation)

---

## 1. Depreciation Methods

Income Tax Act 2007, Section EE 12:

**Diminishing Value (DV):**
- Higher deductions in early years, decreasing over time
- Formula: `adjusted tax value x DV rate`
- Adjusted tax value = cost - accumulated depreciation

**Straight Line (SL):**
- Equal deductions each year
- Formula: `cost x SL rate`

Both methods give the same total deduction over the asset's life.

### Choosing a method:
- DV is more common (bigger deductions early, better cash flow)
- SL is simpler (same amount each year)
- Once chosen for an asset, you cannot switch methods

---

## 2. Low-Value Assets

**Section EE 38 — Low-value assets:**
- Assets costing **$1,000 or less** (GST exclusive): can be expensed immediately (100% deduction in year of purchase)
- This includes most hand tools, safety gear, small equipment
- Assets over $1,000 must be depreciated over their useful life

**Note (from 22 May 2025):** 20% of the cost of new assets can be claimed as an immediate expense, with depreciation applying to the remaining 80%.

---

## 3. Common Builder Asset Depreciation Rates

Source: IRD General Depreciation Rates IR265 (August 2024).

### Motor Vehicles

| Asset | Est. Life | DV Rate | SL Rate |
|-------|-----------|---------|---------|
| Motor vehicles (general) | 5 years | 30% | 21% |
| Utes and light trucks (up to 3.5 tonnes) | 5 years | 30% | 21% |
| Heavy trucks (over 3.5 tonnes) | 8 years | 18% | 12.5% |
| Trailers | 10 years | 13% | 9.5% |

### Power Tools and Equipment

| Asset | Est. Life | DV Rate | SL Rate |
|-------|-----------|---------|---------|
| Portable power tools (drills, saws, grinders) | 5 years | 40% | 30% |
| Fixed/bench power tools | 10 years | 18% | 12.5% |
| Compressors (portable) | 10 years | 18% | 12.5% |
| Concrete mixers (portable) | 8 years | 22% | 15.5% |
| Generators (portable) | 10 years | 18% | 12.5% |
| Welding equipment | 8 years | 22% | 15.5% |
| Nail guns / fastening tools | 5 years | 40% | 30% |
| Laser levels / surveying | 5 years | 40% | 30% |

### Site Equipment

| Asset | Est. Life | DV Rate | SL Rate |
|-------|-----------|---------|---------|
| Scaffolding | 10 years | 13% | 9.5% |
| Ladders (aluminium) | 10 years | 13% | 9.5% |
| Ladders (fibreglass) | 8 years | 18% | 12.5% |
| Temporary fencing | 5 years | 30% | 21% |
| Safety harness systems | 5 years | 30% | 21% |
| Wheelbarrows | 5 years | 40% | 30% |

### Office and Technology

| Asset | Est. Life | DV Rate | SL Rate |
|-------|-----------|---------|---------|
| Computers/laptops | 4 years | 50% | 40% |
| Mobile phones | 3 years | 67% | 67% |
| Printers | 5 years | 40% | 30% |
| Software (general) | 4 years | 50% | 40% |

### Buildings

| Asset | Est. Life | DV Rate | SL Rate |
|-------|-----------|---------|---------|
| Non-residential buildings | - | **0%** | **0%** |

Note: From the 2025 income year, the depreciation rate for non-residential buildings has returned to 0%.

---

## 4. Depreciation Calculation Examples

### Example 1: DeWalt Circular Saw — $899 (portable power tool)

**DV method (40%):**

| Year | Opening Value | Depreciation | Closing Value |
|------|---------------|--------------|---------------|
| 1 | $899.00 | $359.60 | $539.40 |
| 2 | $539.40 | $215.76 | $323.64 |
| 3 | $323.64 | $129.46 | $194.18 |
| 4 | $194.18 | $77.67 | $116.51 |
| 5 | $116.51 | $116.51 | $0.00 |

Note: In the final year, claim the remaining book value.

### Example 2: Toyota Hilux Ute — $45,000

**DV method (30%):**

| Year | Opening Value | Depreciation | Closing Value |
|------|---------------|--------------|---------------|
| 1 | $45,000.00 | $13,500.00 | $31,500.00 |
| 2 | $31,500.00 | $9,450.00 | $22,050.00 |
| 3 | $22,050.00 | $6,615.00 | $15,435.00 |
| 4 | $15,435.00 | $4,630.50 | $10,804.50 |
| 5 | $10,804.50 | $10,804.50 | $0.00 |

If the vehicle is 70% business use, claim 70% of each year's depreciation.

### Example 3: Hand tools under $1,000

A hammer ($65), tape measure ($35), spirit level ($89) — all under $1,000 each. Expense immediately in year of purchase, no depreciation schedule needed.

---

## 5. Disposal of Assets

**Section EE 44 — Depreciation recovery income:**

When you sell or dispose of a depreciated asset:
- If sale price > book value: the difference is **depreciation recovery income** (taxable)
- If sale price < book value: the difference is a **deduction** (loss on disposal)
- If sale price > original cost: excess over cost is a **capital gain** (not taxed for most sole traders under current NZ law, but check bright-line rules for property)

---

## 6. Matching Assets to IRD Categories

When the user adds an asset, match to the closest IRD category:

| User description (keywords) | IRD Category | DV Rate |
|-----------------------------|-------------|---------|
| drill, saw, grinder, sander, router, jigsaw | Portable power tools | 40% |
| nail gun, brad nailer, staple gun | Nail guns / fastening tools | 40% |
| compressor, air compressor | Compressors (portable) | 18% |
| concrete mixer, cement mixer | Concrete mixers (portable) | 22% |
| generator, genset | Generators (portable) | 18% |
| welder, welding | Welding equipment | 22% |
| laser level, dumpy level, theodolite | Laser levels / surveying | 40% |
| scaffolding, scaffold | Scaffolding | 13% |
| ladder | Ladders (aluminium) | 13% |
| ute, truck, van, hilux, ranger, navara | Motor vehicles | 30% |
| trailer | Trailers | 13% |
| computer, laptop, macbook | Computers/laptops | 50% |
| phone, iphone, samsung | Mobile phones | 67% |
| wheelbarrow | Wheelbarrows | 40% |
| harness, safety harness, fall arrest | Safety harness systems | 30% |

---

*Last updated: March 2026. Based on IR265 August 2024. Always verify specific rates using the [IRD depreciation rate finder](https://www.ird.govt.nz/income-tax/income-tax-for-businesses-and-organisations/types-of-business-expenses/depreciation/claiming-depreciation/work-out-your-assets-rate-and-depreciation-value).*
```

**Step 2: Commit**

```bash
git add references/nz-depreciation-rates.md
git commit -m "docs: add NZ depreciation rates reference for builder assets"
```

---

## Task 3: Extend config.json and Data Structures

**Files:**
- Modify: `SKILL.md` — update Data Paths section and add new data structures

**Step 1: Update the Data Paths section in SKILL.md**

Replace the existing Data Paths block with:

```markdown
## Data Paths

```
~/.openclaw/data/kiwi-receipts/
├── config.json        # Business name, GST number, tax settings
├── receipts.json      # All captured purchase receipts
├── income.json        # Sales/invoice records
├── assets.json        # Depreciable assets register
└── tax-history.json   # Previous years' tax figures (for provisional tax)
```

### config.json structure:

```json
{
  "business_name": "My Construction Ltd",
  "gst_number": "12-345-678",
  "balance_date": "31-march",
  "gst_filing_frequency": "2-monthly",
  "depreciation_method": "DV",
  "vehicle_business_percent": 80,
  "phone_business_percent": 70,
  "home_office_percent": 0
}
```

### income.json structure:

Each entry represents an invoice or payment received:

```json
[
  {
    "id": "uuid-here",
    "date": "2026-03-15",
    "client": "ABC Homes Ltd",
    "description": "Bathroom renovation - 42 Rimu St",
    "amount_excl_gst": 8500.00,
    "gst": 1275.00,
    "amount_incl_gst": 9775.00,
    "invoice_number": "INV-2026-015",
    "status": "paid",
    "created_at": "2026-03-15T14:30:00Z"
  }
]
```

### assets.json structure:

```json
[
  {
    "id": "uuid-here",
    "name": "DeWalt DCS570 Circular Saw",
    "category": "portable_power_tools",
    "purchase_date": "2026-01-15",
    "cost": 899.00,
    "dv_rate": 0.40,
    "sl_rate": 0.30,
    "method": "DV",
    "business_percent": 100,
    "disposed": false,
    "disposal_date": null,
    "disposal_amount": null,
    "created_at": "2026-01-15T10:00:00Z"
  }
]
```

### tax-history.json structure:

```json
{
  "years": {
    "2025": {
      "tax_year_end": "2025-03-31",
      "gross_income": 95000.00,
      "total_expenses": 42000.00,
      "depreciation": 3500.00,
      "taxable_income": 49500.00,
      "tax_on_income": 7582.50,
      "acc_levy": 826.50,
      "total_tax": 8409.00,
      "tax_already_paid": 0,
      "residual_income_tax": 8409.00
    }
  }
}
```
```

**Step 2: Commit**

```bash
git add SKILL.md
git commit -m "feat: add data structures for income, assets, and tax history"
```

---

## Task 4: Add Income Tracking Commands to SKILL.md

**Files:**
- Modify: `SKILL.md` — add income commands after the existing text commands section

**Step 1: Add the following sections to SKILL.md after "Handling Text Commands"**

```markdown
## Handling Income / Sales

### "income <amount> <description>" or "收入 <amount> <description>"

Record a sales invoice or payment received:

```
User: income 9775 Bathroom renovation - 42 Rimu St, ABC Homes
```

Parse:
- amount_incl_gst: 9775.00
- gst: 9775 x 3/23 = 1274.35
- amount_excl_gst: 9775 - 1274.35 = 8500.65
- client: extract from description (text after last comma, or ask)
- description: remaining text
- date: today (unless user specifies)

Confirm:
```
Income recorded:
  Client: ABC Homes
  Description: Bathroom renovation - 42 Rimu St
  Amount: $9,775.00 (GST: $1,274.35)
  Date: 2026-03-19

Reply to save, or correct any details.
```

After confirmation, append to `~/.openclaw/data/kiwi-receipts/income.json`.

### "income list" or "收入列表"
Show last 10 income entries with date, client, amount.

### "income summary" or "收入汇总"
Show current GST period income total:
```
Income Summary: Mar-Apr 2026
  Total income (incl GST): $28,500.00
  Total GST on income: $3,717.39
  Invoices: 4
```

### Updated GST report with income

When the user runs "report", if income.json has data for the period, the GST101A sheet now auto-fills BOTH sides:

- Box 5: Total sales and income (from income.json) -- AUTO-FILLED
- Box 6: Zero-rated supplies (default $0)
- Box 7: Box 5 - Box 6 -- auto-calculated
- Box 8: Box 7 x 3/23 -- auto-calculated
- Box 9: Adjustments (default $0)
- Box 10: Box 8 + Box 9 -- auto-calculated
- Box 11: Total purchases (from receipts.json) -- auto-filled (existing)
- Box 12: Box 11 x 3/23 -- auto-calculated (existing)
- Box 13: Credit adjustments (default $0)
- Box 14: Box 12 + Box 13 -- auto-calculated (existing)
- Box 15: Box 10 - Box 14 -- NOW FULLY AUTO-CALCULATED

If income data exists, Box 15 shows the final GST pay/refund amount.
If no income data, Box 5 still shows "enter from accounts" as before.
```

**Step 2: Commit**

```bash
git add SKILL.md
git commit -m "feat: add income tracking commands and GST auto-fill for Box 5"
```

---

## Task 5: Add Asset and Depreciation Commands to SKILL.md

**Files:**
- Modify: `SKILL.md` — add asset tracking section

**Step 1: Add the following section to SKILL.md**

```markdown
## Handling Assets and Depreciation

### "asset add <name> <cost>" or "资产 <name> <cost>"

Record a new business asset:

```
User: asset add DeWalt circular saw $899
```

Parse:
- name: "DeWalt circular saw"
- cost: 899.00 (GST exclusive — if user gives GST-inclusive, extract GST first)
- Match to IRD category using keyword matching from `references/nz-depreciation-rates.md`
- Apply correct DV and SL rates
- Use depreciation method from config (default: DV)

If cost is $1,000 or less (excl GST): inform user this can be expensed immediately, no depreciation needed. Still record it.

Confirm:
```
Asset recorded:
  Name: DeWalt circular saw
  Cost: $899.00 (excl GST)
  Category: Portable power tools
  Depreciation: DV 40% (estimated life 5 years)
  Year 1 claim: $359.60

  This asset costs under $1,000 — you can alternatively expense it
  immediately in the year of purchase. Reply "expense" to do that,
  or "depreciate" to spread over 5 years.
```

Save to `~/.openclaw/data/kiwi-receipts/assets.json`.

### "asset list" or "资产列表"
Show all assets with current book value:
```
Assets Register:
  1. DeWalt circular saw — cost $899, book value $539.40 (DV 40%)
  2. Toyota Hilux — cost $45,000, book value $31,500.00 (DV 30%)
  3. Scaffolding set — cost $3,200, book value $2,784.00 (DV 13%)
```

### "asset dispose <name> <sale price>" or "资产处置 <name> <price>"
Mark an asset as disposed. Calculate depreciation recovery or loss:
```
User: asset dispose DeWalt circular saw $200
Bot: Asset disposed:
     DeWalt circular saw
     Book value: $539.40
     Sale price: $200.00
     Loss on disposal: $339.40 (deductible)
```

### "depreciation" or "折旧"
Calculate this year's total depreciation for all active assets:
```
Depreciation Schedule 2025-2026:
  DeWalt circular saw: $215.76 (DV 40%, book: $539.40 -> $323.64)
  Toyota Hilux (70% business): $6,615.00 x 70% = $4,630.50
  Scaffolding set: $416.00

  Total depreciation: $5,262.26
```

### Depreciation calculation logic:

For each active (non-disposed) asset:

**DV method:**
```
book_value = cost
for each completed year since purchase:
    depreciation = book_value * dv_rate
    book_value = book_value - depreciation
current_year_depreciation = book_value * dv_rate * business_percent/100
```

**SL method:**
```
annual_depreciation = cost * sl_rate
current_year_depreciation = annual_depreciation * business_percent/100
```

**Partial year:** If purchased part-way through the tax year (April-March), pro-rate:
```
months_owned = months from purchase date to 31 March (or today)
partial_rate = months_owned / 12
depreciation = full_year_depreciation * partial_rate
```
```

**Step 2: Commit**

```bash
git add SKILL.md
git commit -m "feat: add asset tracking and depreciation commands"
```

---

## Task 6: Add Provisional Tax and IR3 Commands to SKILL.md

**Files:**
- Modify: `SKILL.md` — add tax calculation commands

**Step 1: Add the following section to SKILL.md**

```markdown
## Provisional Tax

### "provisional" or "预缴税"

Calculate provisional tax based on tax history:

1. Read `tax-history.json` for previous year's residual income tax (RIT)
2. If RIT <= $5,000: "You don't need to pay provisional tax (RIT under $5,000)"
3. If RIT > $5,000:

```
Provisional Tax 2026-2027:
  Based on 2025-2026 RIT: $8,409.00
  Uplift (x 1.05): $8,829.45
  Per instalment: $2,943.15

  Payment schedule:
    1st instalment: 28 August 2026 — $2,943.15
    2nd instalment: 15 January 2027 — $2,943.15
    3rd instalment:  7 May 2027    — $2,943.15
```

### "set last year tax <amount>" or "去年税 <amount>"

Set the previous year's residual income tax for provisional tax calculation:

```
User: set last year tax 8409
Bot: Saved. Previous year RIT: $8,409.00
     Provisional tax this year: $8,829.45 ($2,943.15 x 3 instalments)
```

Save to `tax-history.json`.

## Annual Income Tax (IR3)

### "tax return" or "ir3" or "年度报税"

Generate a complete annual tax summary. Reads from all data files for the tax year (1 April - 31 March):

```
Annual Tax Summary: 2025-2026

INCOME:
  Gross business income (from invoices):  $95,000.00
  GST on income:                          $12,391.30
  Income excl GST:                        $82,608.70

EXPENSES (from receipts):
  Materials:        $28,500.00
  Tools:             $3,200.00
  Fuel:              $4,800.00
  Vehicle:           $2,100.00
  Safety:            $1,500.00
  Subcontractors:    $8,000.00
  Office:              $900.00
  Other:               $500.00
  Total expenses:   $49,500.00

DEPRECIATION:
  Portable power tools:   $1,200.00
  Motor vehicle (70%):    $4,630.50
  Scaffolding:              $416.00
  Total depreciation:     $6,246.50

TAX CALCULATION:
  Gross income:       $82,608.70
  Less expenses:     -$49,500.00
  Less depreciation: -$6,246.50
  Taxable income:     $26,862.20

  Tax on $26,862.20:
    $15,600 @ 10.5% =  $1,638.00
    $11,262.20 @ 17.5% = $1,970.89
    Total tax:          $3,608.89

  ACC earner's levy:      $448.60
  Less provisional tax:  -$2,943.15
  Tax to pay:             $1,114.34

  Reply "export ir3" to generate the XLSX report.
```

### "export ir3" or "导出年度报税"

Generate XLSX with additional sheets:
- IR3B Summary (business income schedule)
- Depreciation Schedule
- Annual Expense Detail
- Provisional Tax Summary

These are added to the existing XLSX generator.
```

**Step 2: Commit**

```bash
git add SKILL.md
git commit -m "feat: add provisional tax and IR3 annual tax commands"
```

---

## Task 7: Add Xero CSV Export Command to SKILL.md

**Files:**
- Modify: `SKILL.md` — add Xero export section

**Step 1: Add the following section to SKILL.md**

```markdown
## Xero CSV Export

### "xero export" or "导出xero"

Generate a CSV file that can be imported into Xero as bank transactions.

**Xero import format (Manual Journal or Bank Transaction):**

```csv
*Date,*Amount,Payee,Description,Reference,Category
2026-03-15,-174.00,Bunnings Warehouse,Timber 2x4 x10 Concrete Mix x5,,Materials
2026-03-16,-65.00,Z Energy,Fuel,,Fuel
2026-03-17,9775.00,ABC Homes Ltd,Bathroom renovation - INV-2026-015,,Sales
```

The CSV includes:
- All receipts (as negative amounts — purchases)
- All income entries (as positive amounts — sales)
- Category mapping to Xero account names
- Date in Xero-expected format (DD/MM/YYYY)

**Category to Xero account mapping:**

| Kiwi Receipts Category | Xero Account Name |
|------------------------|-------------------|
| materials | Cost of Goods Sold - Materials |
| tools | Tools & Equipment |
| fuel | Motor Vehicle Expenses - Fuel |
| vehicle | Motor Vehicle Expenses |
| safety | Health & Safety |
| subcontractor | Subcontractor Expenses |
| office | Office Expenses |
| other | General Expenses |
| sales (income) | Sales |

```bash
python3 {baseDir}/scripts/generate_report.py \
  --data ~/.openclaw/data/kiwi-receipts/receipts.json \
  --income ~/.openclaw/data/kiwi-receipts/income.json \
  --output /tmp/xero-export.csv \
  --format xero-csv \
  --period current
```

Send the CSV file to the user.

User imports into Xero: Accounting > Bank Accounts > [Account] > Import Statement.
```

**Step 2: Commit**

```bash
git add SKILL.md
git commit -m "feat: add Xero CSV export command"
```

---

## Task 8: Extend generate_report.py — Income Support

**Files:**
- Modify: `scripts/generate_report.py`

**Step 1: Add --income argument and income loading**

Add to argparse:
```python
parser.add_argument("--income", default="", help="Path to income.json")
```

Add income loading after receipt loading:
```python
income_records = []
if args.income:
    income_path = Path(args.income)
    if income_path.exists():
        with open(income_path) as f:
            all_income = json.load(f)
        income_records = filter_by_period(all_income, args.period)
```

**Step 2: Update add_ird_sheet to auto-fill Box 5 when income data exists**

Replace the Box 5 and related rows:
```python
def add_ird_sheet(wb: Workbook, receipts: list, period_str: str, income: list = None):
    # ... existing setup ...

    # Box 11: total purchases incl GST
    box_11 = round(sum(r.get("total", 0) for r in receipts), 2)
    box_12 = round(box_11 * 3 / 23, 2)
    box_14 = box_12

    # Box 5: total sales incl GST (from income if available)
    if income:
        box_5 = round(sum(r.get("amount_incl_gst", 0) for r in income), 2)
        box_6 = 0.00
        box_7 = box_5 - box_6
        box_8 = round(box_7 * 3 / 23, 2)
        box_9 = 0.00
        box_10 = box_8 + box_9
        box_15 = round(box_10 - box_14, 2)
        box_5_display = box_5
        box_7_display = box_7
        box_8_display = box_8
        box_10_display = box_10
        box_15_display = box_15
    else:
        box_5_display = "-- enter from accounts --"
        box_7_display = "-- calculated --"
        box_8_display = "-- calculated --"
        box_10_display = "-- calculated --"
        box_15_display = "-- calculated --"

    ird_rows = [
        ("5", "Total sales and income for the period (incl GST and zero-rated supplies)", box_5_display),
        ("6", "Zero-rated supplies included in Box 5", 0.00),
        ("7", "Box 5 minus Box 6", box_7_display),
        ("8", "Multiply Box 7 by three and divide by twenty-three (x 3/23)", box_8_display),
        ("9", "Adjustments from your calculation sheet", 0.00),
        ("10", "Total GST collected on sales and income (Box 8 + Box 9)", box_10_display),
        ("", "", ""),
        ("11", "Total purchases and expenses (incl GST), excl imported goods", box_11),
        ("12", "Multiply Box 11 by three and divide by twenty-three (x 3/23)", box_12),
        ("13", "Credit adjustments from your calculation sheet", 0.00),
        ("14", "Total GST credit for purchases and expenses (Box 12 + Box 13)", box_14),
        ("", "", ""),
        ("15", "Difference (Box 10 minus Box 14). Positive = pay, Negative = refund", box_15_display),
    ]
    # ... rest unchanged ...
```

**Step 3: Add income sheet**

```python
def add_income_sheet(wb: Workbook, income: list):
    ws = wb.create_sheet("Income")
    headers = ["Date", "Client", "Description", "Invoice #", "Amount (excl GST)", "GST", "Total (incl GST)"]
    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 25
    ws.column_dimensions["C"].width = 35
    ws.column_dimensions["D"].width = 15
    ws.column_dimensions["E"].width = 18
    ws.column_dimensions["F"].width = 12
    ws.column_dimensions["G"].width = 18

    for col, h in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=h)
    style_header_row(ws, 1, len(headers))

    sorted_income = sorted(income, key=lambda r: r.get("date", ""))
    for i, r in enumerate(sorted_income, start=2):
        ws.cell(row=i, column=1, value=r.get("date", ""))
        ws.cell(row=i, column=2, value=r.get("client", ""))
        ws.cell(row=i, column=3, value=r.get("description", ""))
        ws.cell(row=i, column=4, value=r.get("invoice_number", ""))
        ws.cell(row=i, column=5, value=r.get("amount_excl_gst", 0)).number_format = CURRENCY_FMT
        ws.cell(row=i, column=6, value=r.get("gst", 0)).number_format = CURRENCY_FMT
        ws.cell(row=i, column=7, value=r.get("amount_incl_gst", 0)).number_format = CURRENCY_FMT
        for col in range(1, 8):
            ws.cell(row=i, column=col).border = THIN_BORDER
```

**Step 4: Wire income into main()**

Update the main function to load income, pass to sheets, and call add_income_sheet:
```python
# In main(), after loading receipts:
income_records = []
if args.income:
    income_path = Path(args.income)
    if income_path.exists():
        with open(income_path) as f:
            all_income = json.load(f)
        income_records = filter_by_period(all_income, args.period)

# Update sheet calls:
add_ird_sheet(wb, receipts, p_label, income_records)
if income_records:
    add_income_sheet(wb, income_records)
```

**Step 5: Test with sample data and commit**

Create test income data, generate report, verify Box 5 is filled and Box 15 is calculated.

```bash
git add scripts/generate_report.py
git commit -m "feat: add income tracking and auto-fill GST101A Box 5"
```

---

## Task 9: Extend generate_report.py — Depreciation Schedule Sheet

**Files:**
- Modify: `scripts/generate_report.py`

**Step 1: Add --assets argument**

```python
parser.add_argument("--assets", default="", help="Path to assets.json")
```

**Step 2: Add depreciation calculation functions**

```python
def calculate_depreciation(asset: dict, tax_year_end: date) -> dict:
    """Calculate current year depreciation for an asset."""
    purchase = date.fromisoformat(asset["purchase_date"])
    cost = asset["cost"]
    method = asset.get("method", "DV")
    dv_rate = asset.get("dv_rate", 0)
    sl_rate = asset.get("sl_rate", 0)
    business_pct = asset.get("business_percent", 100) / 100
    disposed = asset.get("disposed", False)

    tax_year_start = date(tax_year_end.year - 1, 4, 1)

    if disposed:
        disposal_date = date.fromisoformat(asset.get("disposal_date", str(tax_year_end)))
        if disposal_date < tax_year_start:
            return {"depreciation": 0, "book_value_start": 0, "book_value_end": 0}

    # Calculate book value at start of current tax year
    book_value = cost
    current = date(purchase.year, 4, 1) if purchase.month >= 4 else date(purchase.year - 1, 4, 1)

    while current < tax_year_start and book_value > 0:
        next_year = date(current.year + 1, 3, 31)
        if current <= purchase:
            # First year: pro-rate
            months = min(12, (next_year - purchase).days * 12 // 365)
            months = max(1, months)
        else:
            months = 12

        if method == "DV":
            annual = book_value * dv_rate
        else:
            annual = cost * sl_rate

        dep = annual * months / 12
        book_value = max(0, book_value - dep)
        current = date(current.year + 1, 4, 1)

    book_value_start = round(book_value, 2)

    # Current year
    if purchase >= tax_year_start:
        months = min(12, (tax_year_end - purchase).days * 12 // 365)
        months = max(1, months)
    else:
        months = 12

    if method == "DV":
        annual = book_value * dv_rate
    else:
        annual = cost * sl_rate

    dep = round(annual * months / 12, 2)
    dep_business = round(dep * business_pct, 2)
    book_value_end = round(max(0, book_value - dep), 2)

    return {
        "depreciation_full": dep,
        "depreciation_business": dep_business,
        "book_value_start": book_value_start,
        "book_value_end": book_value_end,
    }
```

**Step 3: Add depreciation sheet**

```python
def add_depreciation_sheet(wb: Workbook, assets: list, tax_year_end: date):
    ws = wb.create_sheet("Depreciation")
    headers = ["Asset", "Category", "Purchase Date", "Cost", "Method",
               "Rate", "Business %", "Opening Value", "Depreciation", "Closing Value"]
    widths = [30, 22, 14, 14, 10, 10, 12, 16, 16, 16]
    for col, (h, w) in enumerate(zip(headers, widths), 1):
        ws.cell(row=1, column=col, value=h)
        ws.column_dimensions[chr(64 + col)].width = w
    style_header_row(ws, 1, len(headers))

    total_dep = 0
    active_assets = [a for a in assets if not a.get("disposed", False)]

    for i, asset in enumerate(sorted(active_assets, key=lambda a: a.get("name", "")), start=2):
        dep = calculate_depreciation(asset, tax_year_end)
        total_dep += dep["depreciation_business"]

        rate = asset.get("dv_rate", 0) if asset.get("method", "DV") == "DV" else asset.get("sl_rate", 0)

        ws.cell(row=i, column=1, value=asset.get("name", ""))
        ws.cell(row=i, column=2, value=asset.get("category", ""))
        ws.cell(row=i, column=3, value=asset.get("purchase_date", ""))
        ws.cell(row=i, column=4, value=asset.get("cost", 0)).number_format = CURRENCY_FMT
        ws.cell(row=i, column=5, value=asset.get("method", "DV"))
        ws.cell(row=i, column=6, value=f"{rate*100:.0f}%")
        ws.cell(row=i, column=7, value=f"{asset.get('business_percent', 100)}%")
        ws.cell(row=i, column=8, value=dep["book_value_start"]).number_format = CURRENCY_FMT
        ws.cell(row=i, column=9, value=dep["depreciation_business"]).number_format = CURRENCY_FMT
        ws.cell(row=i, column=10, value=dep["book_value_end"]).number_format = CURRENCY_FMT

        for col in range(1, 11):
            ws.cell(row=i, column=col).border = THIN_BORDER

    # Total row
    total_row = len(active_assets) + 2
    ws.cell(row=total_row, column=8, value="TOTAL").font = Font(bold=True)
    ws.cell(row=total_row, column=9, value=round(total_dep, 2)).number_format = CURRENCY_FMT
    ws.cell(row=total_row, column=9).font = Font(bold=True)

    return round(total_dep, 2)
```

**Step 4: Wire into main() and commit**

```bash
git add scripts/generate_report.py
git commit -m "feat: add depreciation schedule sheet to XLSX report"
```

---

## Task 10: Extend generate_report.py — IR3 Annual Tax Sheet

**Files:**
- Modify: `scripts/generate_report.py`

**Step 1: Add tax calculation function**

```python
NZ_TAX_BRACKETS = [
    (15600, 0.105),
    (53500, 0.175),
    (78100, 0.30),
    (180000, 0.33),
    (float("inf"), 0.39),
]
ACC_LEVY_RATE = 0.0167
ACC_MAX_EARNINGS = 152790

def calculate_income_tax(taxable_income: float) -> float:
    """Calculate NZ income tax using progressive brackets."""
    tax = 0
    prev_threshold = 0
    for threshold, rate in NZ_TAX_BRACKETS:
        if taxable_income <= prev_threshold:
            break
        bracket_income = min(taxable_income, threshold) - prev_threshold
        tax += bracket_income * rate
        prev_threshold = threshold
    return round(tax, 2)

def calculate_acc_levy(gross_income: float) -> float:
    """Calculate ACC earner's levy."""
    insurable = min(gross_income, ACC_MAX_EARNINGS)
    return round(insurable * ACC_LEVY_RATE, 2)
```

**Step 2: Add IR3 summary sheet**

```python
def add_ir3_sheet(wb: Workbook, receipts: list, income: list, total_depreciation: float,
                  tax_year: str, business_name: str, gst_number: str,
                  tax_history: dict = None):
    ws = wb.create_sheet("IR3 Annual Tax")
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions["B"].width = 20

    # Calculate totals
    gross_income_incl = sum(r.get("amount_incl_gst", 0) for r in income)
    gross_income_excl = sum(r.get("amount_excl_gst", 0) for r in income)

    # Expenses by category
    categories = {}
    for r in receipts:
        cat = r.get("category", "other")
        gst = r.get("gst", 0)
        excl = r.get("total", 0) - gst
        categories[cat] = categories.get(cat, 0) + excl
    total_expenses = round(sum(categories.values()), 2)

    taxable_income = round(gross_income_excl - total_expenses - total_depreciation, 2)
    taxable_income = max(0, taxable_income)
    income_tax = calculate_income_tax(taxable_income)
    acc_levy = calculate_acc_levy(gross_income_excl)

    provisional_paid = 0
    if tax_history and "years" in tax_history:
        for year_data in tax_history["years"].values():
            provisional_paid += year_data.get("provisional_tax_paid", 0)

    total_tax = income_tax + acc_levy
    tax_to_pay = round(total_tax - provisional_paid, 2)

    ws.cell(row=1, column=1, value=f"Annual Tax Summary: {tax_year}").font = TITLE_FONT
    ws.cell(row=2, column=1, value=business_name).font = Font(italic=True)
    ws.cell(row=3, column=1, value=f"IRD/GST: {gst_number}").font = Font(italic=True)

    row = 5
    ws.cell(row=row, column=1, value="INCOME").font = Font(bold=True, size=12)
    row += 1
    ws.cell(row=row, column=1, value="Gross business income (incl GST)")
    ws.cell(row=row, column=2, value=round(gross_income_incl, 2)).number_format = CURRENCY_FMT
    row += 1
    ws.cell(row=row, column=1, value="Less GST on income")
    ws.cell(row=row, column=2, value=round(gross_income_incl - gross_income_excl, 2)).number_format = CURRENCY_FMT
    row += 1
    ws.cell(row=row, column=1, value="Gross business income (excl GST)").font = Font(bold=True)
    ws.cell(row=row, column=2, value=round(gross_income_excl, 2)).number_format = CURRENCY_FMT
    ws.cell(row=row, column=2).font = Font(bold=True)

    row += 2
    ws.cell(row=row, column=1, value="EXPENSES (excl GST)").font = Font(bold=True, size=12)
    row += 1
    for cat in sorted(categories.keys()):
        ws.cell(row=row, column=1, value=f"  {cat.title()}")
        ws.cell(row=row, column=2, value=round(categories[cat], 2)).number_format = CURRENCY_FMT
        row += 1
    ws.cell(row=row, column=1, value="Total expenses").font = Font(bold=True)
    ws.cell(row=row, column=2, value=total_expenses).number_format = CURRENCY_FMT
    ws.cell(row=row, column=2).font = Font(bold=True)

    row += 2
    ws.cell(row=row, column=1, value="DEPRECIATION").font = Font(bold=True, size=12)
    row += 1
    ws.cell(row=row, column=1, value="Total depreciation (see Depreciation sheet)")
    ws.cell(row=row, column=2, value=total_depreciation).number_format = CURRENCY_FMT

    row += 2
    ws.cell(row=row, column=1, value="TAX CALCULATION").font = Font(bold=True, size=12)
    row += 1
    ws.cell(row=row, column=1, value="Gross income (excl GST)")
    ws.cell(row=row, column=2, value=round(gross_income_excl, 2)).number_format = CURRENCY_FMT
    row += 1
    ws.cell(row=row, column=1, value="Less total expenses")
    ws.cell(row=row, column=2, value=-total_expenses).number_format = CURRENCY_FMT
    row += 1
    ws.cell(row=row, column=1, value="Less depreciation")
    ws.cell(row=row, column=2, value=-total_depreciation).number_format = CURRENCY_FMT
    row += 1
    ws.cell(row=row, column=1, value="Taxable income").font = Font(bold=True)
    ws.cell(row=row, column=2, value=taxable_income).number_format = CURRENCY_FMT
    ws.cell(row=row, column=2).font = Font(bold=True)

    row += 2
    ws.cell(row=row, column=1, value="Income tax").font = Font(bold=True)
    ws.cell(row=row, column=2, value=income_tax).number_format = CURRENCY_FMT
    ws.cell(row=row, column=2).font = Font(bold=True)
    row += 1

    # Show bracket breakdown
    prev_t = 0
    for threshold, rate in NZ_TAX_BRACKETS:
        if taxable_income <= prev_t:
            break
        bracket = min(taxable_income, threshold) - prev_t
        bracket_tax = round(bracket * rate, 2)
        ws.cell(row=row, column=1, value=f"  ${prev_t:,.0f} - ${min(taxable_income, threshold):,.0f} @ {rate*100:.1f}%")
        ws.cell(row=row, column=2, value=bracket_tax).number_format = CURRENCY_FMT
        row += 1
        prev_t = threshold

    row += 1
    ws.cell(row=row, column=1, value="ACC earner's levy (1.67%)")
    ws.cell(row=row, column=2, value=acc_levy).number_format = CURRENCY_FMT
    row += 1
    ws.cell(row=row, column=1, value="Total tax + ACC").font = Font(bold=True)
    ws.cell(row=row, column=2, value=total_tax).number_format = CURRENCY_FMT
    ws.cell(row=row, column=2).font = Font(bold=True)

    if provisional_paid > 0:
        row += 1
        ws.cell(row=row, column=1, value="Less provisional tax paid")
        ws.cell(row=row, column=2, value=-provisional_paid).number_format = CURRENCY_FMT

    row += 2
    ws.cell(row=row, column=1, value="TAX TO PAY (or REFUND if negative)").font = Font(bold=True, size=12)
    ws.cell(row=row, column=2, value=tax_to_pay).number_format = CURRENCY_FMT
    ws.cell(row=row, column=2).font = Font(bold=True, size=12)

    # Borders for all data cells
    for r in range(1, row + 1):
        for c in range(1, 3):
            ws.cell(row=r, column=c).border = THIN_BORDER
```

**Step 3: Wire into main() with --tax-history and --assets flags and commit**

```bash
git add scripts/generate_report.py
git commit -m "feat: add IR3 annual tax summary sheet with bracket calculation"
```

---

## Task 11: Add Xero CSV Export to generate_report.py

**Files:**
- Modify: `scripts/generate_report.py`

**Step 1: Add --format argument**

```python
parser.add_argument("--format", default="xlsx", choices=["xlsx", "xero-csv"],
                    help="Output format: xlsx or xero-csv")
```

**Step 2: Add Xero CSV generator**

```python
import csv

XERO_CATEGORY_MAP = {
    "materials": "Cost of Goods Sold - Materials",
    "tools": "Tools & Equipment",
    "fuel": "Motor Vehicle Expenses - Fuel",
    "vehicle": "Motor Vehicle Expenses",
    "safety": "Health & Safety",
    "subcontractor": "Subcontractor Expenses",
    "office": "Office Expenses",
    "other": "General Expenses",
}

def generate_xero_csv(receipts: list, income: list, output_path: Path):
    """Generate Xero-importable CSV with purchases and income."""
    rows = []

    for r in receipts:
        dt = r.get("date", "")
        try:
            d = date.fromisoformat(dt)
            formatted_date = d.strftime("%d/%m/%Y")
        except ValueError:
            formatted_date = dt

        items_desc = ", ".join(
            item.get("description", "") for item in r.get("items", [])
        ) or r.get("merchant", "")

        rows.append({
            "Date": formatted_date,
            "Amount": -r.get("total", 0),
            "Payee": r.get("merchant", ""),
            "Description": items_desc,
            "Reference": r.get("id", ""),
            "Category": XERO_CATEGORY_MAP.get(r.get("category", "other"), "General Expenses"),
        })

    for r in income:
        dt = r.get("date", "")
        try:
            d = date.fromisoformat(dt)
            formatted_date = d.strftime("%d/%m/%Y")
        except ValueError:
            formatted_date = dt

        rows.append({
            "Date": formatted_date,
            "Amount": r.get("amount_incl_gst", 0),
            "Payee": r.get("client", ""),
            "Description": r.get("description", ""),
            "Reference": r.get("invoice_number", ""),
            "Category": "Sales",
        })

    rows.sort(key=lambda x: x["Date"])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Date", "Amount", "Payee", "Description", "Reference", "Category"])
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps({
        "format": "xero-csv",
        "transactions": len(rows),
        "output": str(output_path),
    }))
```

**Step 3: Branch in main() based on --format**

```python
if args.format == "xero-csv":
    generate_xero_csv(receipts, income_records, Path(args.output))
else:
    # existing XLSX generation
    ...
```

**Step 4: Test and commit**

```bash
git add scripts/generate_report.py
git commit -m "feat: add Xero CSV export format"
```

---

## Task 12: Update SKILL.md — Compliance Rules for Income Tax

**Files:**
- Modify: `SKILL.md` — extend Compliance Rules section

**Step 1: Add income tax compliance rules after the existing GST compliance rules**

```markdown
## Income Tax Compliance Rules

Per the Income Tax Act 2007 and Tax Administration Act 1994:

### Tax Calculation (Schedule 1, Part A)
27. NZ income tax uses **progressive brackets** -- each bracket applies only to income within that range
28. Current rates (from 1 April 2025): 10.5% / 17.5% / 30% / 33% / 39%
29. ACC earner's levy: **1.67%** of gross earnings, capped at $152,790 insurable earnings
30. Sole traders pay income tax on **net profit** (income - expenses - depreciation)

### Business Expenses (Section DA 1)
31. A deduction is allowed to the extent it is incurred in **deriving assessable income**
32. Capital expenditure is NOT deductible -- must be **depreciated** (Section DA 2)
33. Mixed-use assets (vehicle, phone, home office) must be **apportioned** to business %
34. Entertainment expenses: only **50% deductible** for client meals

### Depreciation (Subpart EE)
35. Assets over **$1,000** (excl GST) must be depreciated, not expensed
36. Assets **$1,000 or less** can be expensed immediately in year of purchase
37. Two methods: **DV** (diminishing value) or **SL** (straight line)
38. Rates are set by IRD in **IR265** -- match asset to closest IRD category
39. Partial year: pro-rate depreciation based on months owned in the tax year
40. On disposal: if sale price > book value, difference is **depreciation recovery income** (taxable)

### Provisional Tax (Part RC)
41. Required when previous year residual income tax exceeds **$5,000**
42. Standard method: previous year RIT x **105%**, divided into 3 instalments
43. Payment dates (March balance date): **28 Aug**, **15 Jan**, **7 May**
44. If previous year return not filed, use 2-year-ago RIT x **110%**

### Filing (Tax Administration Act 1994)
45. IR3 due **7 July** (self-filing) or **31 March following year** (via tax agent)
46. Tax year runs **1 April to 31 March**
47. Keep all records for **minimum 7 years** (same as GST)

### Disclaimers
48. **Always state**: "This is a calculation tool, not tax advice. Verify with a qualified accountant before filing."
49. **Do not recommend** business structure changes (sole trader vs company vs trust)
50. **Do not advise** on tax minimization strategies beyond standard deductions
```

**Step 2: Commit**

```bash
git add SKILL.md
git commit -m "docs: add income tax compliance rules to SKILL.md"
```

---

## Task 13: Update README.md

**Files:**
- Modify: `README.md`

**Step 1: Rewrite README with all new features**

Update the README to reflect all new features:
- Income tracking (sales/invoices)
- Full GST101A auto-fill (both sides)
- IR3 annual tax calculation
- Provisional tax calculation
- Asset depreciation tracking
- Xero CSV export
- Updated commands table
- Updated file structure
- Updated legal compliance section

Remove all emoji from the README. Keep it factual and professional.

Key sections to update:
- Features list: add income tracking, IR3, provisional tax, depreciation, Xero CSV
- How It Works: add annual workflow alongside the existing 2-monthly GST workflow
- Commands table: add all new commands
- GST101A Box Mapping: update to show Box 5 can now be auto-filled
- File Structure: add new data files and reference docs
- Legal Compliance: add Income Tax Act 2007 and depreciation references

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update README with full tax coverage features"
```

---

## Task 14: Test All Features End-to-End

**Files:**
- No new files -- testing existing code

**Step 1: Create comprehensive test data**

Create test files in `/tmp/kiwi-test-v2/`:
- `receipts.json` — 10+ receipts across categories
- `income.json` — 5+ invoices
- `assets.json` — 3-4 assets (ute, power tools, scaffolding)
- `tax-history.json` — one previous year with RIT > $5,000
- `config.json` — full config with business percentages

**Step 2: Test GST report with income (auto-fill both sides)**

```bash
python3 scripts/generate_report.py \
  --data /tmp/kiwi-test-v2/receipts.json \
  --income /tmp/kiwi-test-v2/income.json \
  --output /tmp/kiwi-test-v2/gst-report.xlsx \
  --period current \
  --business-name "Test Construction Ltd" \
  --gst-number "12-345-678"
```

Verify:
- IRD GST101A sheet: Box 5 is filled, Box 15 is calculated
- Income sheet exists with all invoice data

**Step 3: Test annual report with all data**

```bash
python3 scripts/generate_report.py \
  --data /tmp/kiwi-test-v2/receipts.json \
  --income /tmp/kiwi-test-v2/income.json \
  --assets /tmp/kiwi-test-v2/assets.json \
  --tax-history /tmp/kiwi-test-v2/tax-history.json \
  --output /tmp/kiwi-test-v2/annual-report.xlsx \
  --period all \
  --business-name "Test Construction Ltd" \
  --gst-number "12-345-678"
```

Verify:
- Depreciation sheet with correct calculations
- IR3 Annual Tax sheet with correct bracket calculation
- All amounts add up correctly

**Step 4: Test Xero CSV export**

```bash
python3 scripts/generate_report.py \
  --data /tmp/kiwi-test-v2/receipts.json \
  --income /tmp/kiwi-test-v2/income.json \
  --output /tmp/kiwi-test-v2/xero-export.csv \
  --format xero-csv \
  --period current
```

Verify:
- CSV has correct headers
- Purchases are negative, income is positive
- Dates in DD/MM/YYYY format
- Categories mapped correctly

**Step 5: Commit test results**

```bash
git add -A
git commit -m "test: verify all v2 features end-to-end"
```

---

## Task 15: Publish v2.0.0

**Step 1: Push to GitHub**

```bash
git push
```

**Step 2: Publish to ClawHub**

```bash
clawhub publish . --slug kiwi-receipts --name "Kiwi Receipts" --version 2.0.0 \
  --changelog "v2.0: Full NZ tax coverage — income tracking, IR3 annual tax, provisional tax, depreciation, Xero CSV export" \
  --tags latest
```

**Step 3: Verify on ClawHub page**

Check https://clawhub.ai/maxazure/kiwi-receipts for any warnings.

---

## Summary of New Commands

| Command | Description |
|---------|-------------|
| `income <amount> <desc>` | Record a sales invoice |
| `income list` | Show recent income entries |
| `income summary` | Current period income total |
| `asset add <name> <cost>` | Register a depreciable asset |
| `asset list` | Show assets with book values |
| `asset dispose <name> <price>` | Record asset disposal |
| `depreciation` | Calculate this year's depreciation |
| `provisional` | Calculate provisional tax instalments |
| `set last year tax <amount>` | Set previous year RIT |
| `tax return` / `ir3` | Generate annual tax summary |
| `export ir3` | Generate annual XLSX report |
| `xero export` | Generate Xero-importable CSV |

## New Data Files

| File | Purpose |
|------|---------|
| `income.json` | Sales/invoice records |
| `assets.json` | Depreciable assets register |
| `tax-history.json` | Previous years' tax figures |

## New Reference Docs

| File | Content |
|------|---------|
| `references/nz-income-tax-guide.md` | Tax brackets, IR3, provisional tax, deductions |
| `references/nz-depreciation-rates.md` | IRD depreciation rates for builder assets |
