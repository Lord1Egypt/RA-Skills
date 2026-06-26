---
name: kiwi-receipts
description: "NZ tax assistant for sole traders. Process receipt photos into IRD-ready GST reports, track sales income for GST Box 5, calculate IR3 annual income tax, provisional tax, asset depreciation, and export to Xero CSV. Use when: (1) user sends a receipt/invoice photo, (2) user asks about GST, income tax, or tax returns, (3) user wants to export receipts or generate reports, (4) user mentions IRD, GST, IR3, provisional tax, or depreciation."
metadata:
  {
    "openclaw":
      {
        "emoji": "🧾",
        "triggers": ["receipt", "invoice", "gst", "ird", "tax", "ir3", "depreciation", "provisional", "income", "asset"],
      },
  }
---

# Kiwi Receipts

NZ tax assistant for sole trader builders and contractors. Process receipt photos into IRD-ready GST reports, track sales income, calculate annual income tax (IR3), provisional tax, and asset depreciation. Export to XLSX or Xero CSV.

This is a personal-use skill -- each user runs their own instance. No multi-tenant, no login.

## Data Paths

```
~/.openclaw/data/kiwi-receipts/
├── config.json        # Business name, GST number, tax settings
├── receipts.json      # All captured purchase receipts
├── income.json        # Sales/invoice records
├── assets.json        # Depreciable assets register
└── tax-history.json   # Previous years' tax figures (for provisional tax)
```

## First-Time Setup

When user sends "setup", or on first use when `config.json` doesn't exist:

1. Ask for business name
2. Ask for GST/IRD number
3. Ask for vehicle business use % (default 80)
4. Ask for phone business use % (default 70)
5. Save to `~/.openclaw/data/kiwi-receipts/config.json`:

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

### income.json structure

Each entry represents an invoice or payment received:

```json
[
  {
    "id": "uuid-here",
    "date": "2026-03-15",
    "client": "ABC Homes Ltd",
    "description": "Bathroom renovation - 42 Rimu St",
    "amount_excl_gst": 8500.65,
    "gst": 1274.35,
    "amount_incl_gst": 9775.00,
    "invoice_number": "INV-2026-015",
    "status": "paid",
    "created_at": "2026-03-15T14:30:00Z"
  }
]
```

### assets.json structure

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

### tax-history.json structure

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

## Handling Receipt Photos

When the user sends an image (check for `MediaPaths` in context):

### Step 1: Analyze the image

Use your vision capabilities to analyze the receipt image. Extract:

```json
{
  "merchant": "Bunnings Warehouse",
  "date": "2026-03-15",
  "items": [
    { "description": "Timber 2x4 3.6m", "quantity": 10, "unit_price": 12.50, "amount": 125.00 },
    { "description": "Concrete Mix 40kg", "quantity": 5, "unit_price": 9.80, "amount": 49.00 }
  ],
  "subtotal": 174.00,
  "gst": 22.57,
  "total": 174.00,
  "gst_number": "123-456-789",
  "payment_method": "EFTPOS",
  "category": "materials"
}
```

**Extraction rules:**
- NZ GST is 15%. If only total is visible, calculate GST as `total × 3/23`
- If GST is shown separately on the receipt, use that value
- Detect the GST number if printed on the receipt
- Classify into categories: `materials`, `tools`, `fuel`, `safety`, `subcontractor`, `office`, `vehicle`, `other`
- Dates: parse to ISO format (YYYY-MM-DD), assume current year if not shown
- All amounts in NZD

### Step 2: Confirm with user

Send back a summary:

```
Receipt captured:
  Merchant: Bunnings Warehouse
  Date: 2026-03-15
  Total: $174.00 (GST: $22.57)
  Items: Timber 2x4 3.6m x10, Concrete Mix 40kg x5
  Category: materials

Reply to save, or correct any details.
```

### Step 3: Save receipt data

After confirmation, append to `~/.openclaw/data/kiwi-receipts/receipts.json`:

```bash
mkdir -p ~/.openclaw/data/kiwi-receipts
```

Read existing `receipts.json` (or start with `[]`), append the new receipt with a generated UUID as `id`, and write back. Each receipt object:

```json
{
  "id": "uuid-here",
  "merchant": "...",
  "date": "2026-03-15",
  "items": [...],
  "subtotal": 174.00,
  "gst": 22.57,
  "total": 174.00,
  "gst_number": "...",
  "category": "materials",
  "payment_method": "EFTPOS",
  "created_at": "2026-03-15T10:30:00Z"
}
```

## Handling Text Commands

### "setup"
Create or update `config.json` with business name and GST number.

### "summary"
Read `receipts.json`, filter to current GST period, show:
```
GST Period: Mar-Apr 2026
Total purchases: $1,527.37
Total GST claimable: $199.13
Receipts: 5

By category:
  Materials: $882.97 (GST: $115.17)
  Tools: $114.00 (GST: $14.87)
  Fuel: $131.40 (GST: $17.14)
  Safety: $399.00 (GST: $51.95)
```

### "report" or "export"
Generate and send XLSX report:

```bash
python3 {baseDir}/scripts/generate_report.py \
  --data ~/.openclaw/data/kiwi-receipts/receipts.json \
  --income ~/.openclaw/data/kiwi-receipts/income.json \
  --assets ~/.openclaw/data/kiwi-receipts/assets.json \
  --tax-history ~/.openclaw/data/kiwi-receipts/tax-history.json \
  --output /tmp/gst-report.xlsx \
  --period current \
  --business-name "from config.json" \
  --gst-number "from config.json"
```

Then send the file back to user via message tool with `sendAttachment` action.

### "report YYYY-MM"
Generate report for a specific GST period (the 2-month period containing that month).

**XLSX report contains up to 7 sheets:**

1. **GST Summary** -- Business info, period, total purchases/GST
2. **All Receipts** -- Date, merchant, category, items, amounts
3. **By Category** -- materials/tools/fuel/safety/etc. subtotals
4. **IRD GST101A** -- Pre-filled with official box numbers (see below)
5. **Income** -- Sales/invoice records (if income.json has data)
6. **Depreciation** -- Asset depreciation schedule (if assets.json has data)
7. **IR3 Annual Tax** -- Annual income tax summary (when period=all or period=annual)

**GST101A auto-fill logic:**

If income.json has data for the period, BOTH sides are auto-filled:
- Box 5: Total sales and income (from income.json) -- AUTO-FILLED
- Box 6: Zero-rated supplies (default $0)
- Box 7: Box 5 - Box 6 -- auto-calculated
- Box 8: Box 7 x 3/23 -- auto-calculated
- Box 9: Adjustments (default $0)
- Box 10: Total GST collected (Box 8 + Box 9) -- auto-calculated
- Box 11: Total purchases incl GST (from receipts.json) -- auto-filled
- Box 12: Box 11 x 3/23 -- auto-calculated
- Box 13: Credit adjustments (default $0)
- Box 14: Total GST credit (Box 12 + Box 13) -- auto-calculated
- Box 15: Box 10 - Box 14 -- FULLY AUTO-CALCULATED

If no income data exists, Box 5 still shows "enter from accounts" as before.

### "delete last"
Remove the most recently added receipt from `receipts.json`.

### "list"
Show recent receipts (last 10) with date, merchant, total.

### "help"
```
Kiwi Receipts -- Commands:

RECEIPTS:
  [Send photo]     Capture a receipt
  "summary"        Current GST period overview
  "report"         Download GST report (XLSX)
  "report 2026-03" Report for specific period
  "list"           Show recent receipts
  "delete last"    Remove last receipt

INCOME:
  "income 9775 description"  Record sales invoice
  "income list"              Show recent income
  "income summary"           Period income total

ASSETS:
  "asset add name $cost"     Register depreciable asset
  "asset list"               Show assets with book values
  "asset dispose name $price" Record asset disposal
  "depreciation"             Calculate this year's depreciation

TAX:
  "provisional"              Calculate provisional tax
  "set last year tax 8409"   Set previous year RIT
  "tax return" / "ir3"       Annual tax summary
  "export ir3"               Annual XLSX report

EXPORT:
  "xero export"              Generate Xero-importable CSV

SETUP:
  "setup"                    Configure business details
  "help"                     This message
```

## Handling Income / Sales

### "income [amount] [description]"

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

### "income list"
Show last 10 income entries with date, client, amount.

### "income summary"
Show current GST period income total:
```
Income Summary: Mar-Apr 2026
  Total income (incl GST): $28,500.00
  Total GST on income: $3,717.39
  Invoices: 4
```

## Handling Assets and Depreciation

### "asset add [name] [cost]"

Record a new business asset:

```
User: asset add DeWalt circular saw $899
```

Parse:
- name: "DeWalt circular saw"
- cost: 899.00 (GST exclusive -- if user gives GST-inclusive, extract GST first)
- Match to IRD category using keyword matching from `references/nz-depreciation-rates.md`
- Apply correct DV and SL rates
- Use depreciation method from config (default: DV)

If cost is $1,000 or less (excl GST): inform user this can be expensed immediately. Still record it.

Confirm:
```
Asset recorded:
  Name: DeWalt circular saw
  Cost: $899.00 (excl GST)
  Category: Portable power tools
  Depreciation: DV 40% (estimated life 5 years)
  Year 1 claim: $359.60

  This asset costs under $1,000 -- you can alternatively expense it
  immediately in the year of purchase. Reply "expense" to do that,
  or "depreciate" to spread over 5 years.
```

Save to `~/.openclaw/data/kiwi-receipts/assets.json`.

### "asset list"
Show all assets with current book value:
```
Assets Register:
  1. DeWalt circular saw -- cost $899, book value $539.40 (DV 40%)
  2. Toyota Hilux -- cost $45,000, book value $31,500.00 (DV 30%)
  3. Scaffolding set -- cost $3,200, book value $2,784.00 (DV 13%)
```

### "asset dispose [name] [sale price]"
Mark an asset as disposed. Calculate depreciation recovery or loss:
```
User: asset dispose DeWalt circular saw $200
Bot: Asset disposed:
     DeWalt circular saw
     Book value: $539.40
     Sale price: $200.00
     Loss on disposal: $339.40 (deductible)
```

### "depreciation"
Calculate this year's total depreciation for all active assets:
```
Depreciation Schedule 2025-2026:
  DeWalt circular saw: $215.76 (DV 40%, book: $539.40 -> $323.64)
  Toyota Hilux (70% business): $6,615.00 x 70% = $4,630.50
  Scaffolding set: $416.00

  Total depreciation: $5,262.26
```

### Depreciation calculation logic

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

## Provisional Tax

### "provisional"

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
    1st instalment: 28 August 2026 -- $2,943.15
    2nd instalment: 15 January 2027 -- $2,943.15
    3rd instalment:  7 May 2027    -- $2,943.15
```

### "set last year tax [amount]"

Set the previous year's residual income tax for provisional tax calculation:

```
User: set last year tax 8409
Bot: Saved. Previous year RIT: $8,409.00
     Provisional tax this year: $8,829.45 ($2,943.15 x 3 instalments)
```

Save to `tax-history.json`.

## Annual Income Tax (IR3)

### "tax return" or "ir3"

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

### "export ir3"

Generate XLSX with annual sheets added. Run:

```bash
python3 {baseDir}/scripts/generate_report.py \
  --data ~/.openclaw/data/kiwi-receipts/receipts.json \
  --income ~/.openclaw/data/kiwi-receipts/income.json \
  --assets ~/.openclaw/data/kiwi-receipts/assets.json \
  --tax-history ~/.openclaw/data/kiwi-receipts/tax-history.json \
  --output /tmp/annual-tax-report.xlsx \
  --period all \
  --business-name "from config.json" \
  --gst-number "from config.json"
```

## Xero CSV Export

### "xero export"

Generate a CSV file importable into Xero as bank transactions:

```bash
python3 {baseDir}/scripts/generate_report.py \
  --data ~/.openclaw/data/kiwi-receipts/receipts.json \
  --income ~/.openclaw/data/kiwi-receipts/income.json \
  --output /tmp/xero-export.csv \
  --format xero-csv \
  --period current
```

**Xero CSV format:**

```csv
Date,Amount,Payee,Description,Reference,Category
15/03/2026,-174.00,Bunnings Warehouse,"Timber 2x4 x10, Concrete Mix x5",,Cost of Goods Sold - Materials
16/03/2026,-65.00,Z Energy,Fuel,,Motor Vehicle Expenses - Fuel
17/03/2026,9775.00,ABC Homes Ltd,Bathroom renovation - INV-2026-015,,Sales
```

- Receipts as negative amounts (purchases)
- Income as positive amounts (sales)
- Dates in DD/MM/YYYY format (Xero NZ standard)

**Category to Xero account mapping:**

| Kiwi Receipts Category | Xero Account Name |
|------------------------|-------------------|
| materials | Cost of Goods Sold - Materials |
| tools | Tools and Equipment |
| fuel | Motor Vehicle Expenses - Fuel |
| vehicle | Motor Vehicle Expenses |
| safety | Health and Safety |
| subcontractor | Subcontractor Expenses |
| office | Office Expenses |
| other | General Expenses |
| (income) | Sales |

User imports into Xero: Accounting > Bank Accounts > [Account] > Import Statement.

## GST Period Logic

NZ GST periods (2-monthly, most common for small business):
- Period 1: Jan-Feb → due 28 Mar
- Period 2: Mar-Apr → due 28 May
- Period 3: May-Jun → due 28 Jul
- Period 4: Jul-Aug → due 28 Sep
- Period 5: Sep-Oct → due 28 Nov
- Period 6: Nov-Dec → due 28 Jan

## Compliance Rules

Per the Goods and Services Tax Act 1985 (NZ) and IRD guidelines:

### GST Calculation (Section 8, Section 2 "tax fraction")
1. NZ GST standard rate is **15%** — no exceptions for construction
2. Tax fraction is **3/23** — used to extract GST from inclusive prices
3. Box 12 on GST101A = Box 11 × 3/23 (do NOT sum per-receipt GST)
4. Round to **2 decimal places** (Section 24(6): ≤0.5¢ drop, >0.5¢ round up)

### Taxable Supply Information (Section 19F, effective 1 April 2023)
5. **Under $50**: no TSI required (still best practice to keep receipt)
6. **$50–$200**: need supplier name, date, description, total amount
7. **$200–$1,000**: also need supplier's GST/IRD number + GST shown or "incl GST" statement
8. **Over $1,000**: also need buyer's name + address/phone/email
9. **Don't guess GST numbers** — only record if clearly visible on receipt
10. Supplier must provide TSI within **28 days** of request

### Input Tax Deduction (Section 20(3))
11. Only claim GST on **business** expenses — mixed use must be apportioned
12. Only claim GST from **registered** suppliers (check for GST number)
13. Do NOT claim GST on exempt supplies (residential rent, financial services)
14. **Fuel**: if vehicle has mixed personal/business use, apportion accordingly
15. **Second-hand goods** from unregistered seller: can claim input tax as lesser of purchase price × 3/23 or market value × 3/23 (Section 3A(1)(c))

### Record Keeping (Section 75)
16. Retain all records for **minimum 7 years** (Commissioner may extend to 10)
17. Records must be in **English** and kept **in New Zealand**
18. Electronic records (photos, JSON, XLSX) are acceptable if complete and legible

### Filing (Section 15, 16)
19. GST returns filed electronically via **myIR** (ird.govt.nz)
20. Due by **28th of the month** following period end, except:
    - March period → due **7 May**
    - November period → due **15 January**
21. Late filing penalty: **$50–$250** per return
22. Late payment: **1% immediate** + **4% after 7 days** + interest at ~10.91% p.a.

### General
23. **Always confirm** before saving -- OCR can make mistakes
24. **Category matters** -- ask user if unclear
25. **Keep it conversational** -- concise, friendly, chat-native
26. **Foreign currency**: not directly claimable -- convert to NZD at supply date rate

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
