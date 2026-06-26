# Kiwi Receipts

An [OpenClaw](https://github.com/nichochar/openclaw) skill that serves as a personal NZ tax assistant for sole trader builders and contractors. Processes receipt photos, tracks sales income, calculates GST, income tax, provisional tax, and asset depreciation. Generates IRD-ready XLSX reports and Xero-importable CSV.

## Features

- **Receipt capture** -- snap a photo of any receipt, AI extracts merchant, date, items, GST
- **Sales/income tracking** -- record invoices to auto-fill GST Box 5
- **GST reports** -- XLSX with IRD GST101A pre-filled (both purchases and sales sides)
- **IR3 annual income tax** -- calculates taxable income, applies NZ tax brackets, ACC levy
- **Provisional tax** -- calculates instalments based on previous year RIT
- **Asset depreciation** -- tracks assets, applies IRD DV/SL rates, generates schedules
- **Xero CSV export** -- importable bank transaction format for Xero accounting
- **NZ tax compliant** -- built against GST Act 1985, Income Tax Act 2007, IR265 depreciation rates
- **Personal use** -- runs on your own OpenClaw instance, all data stays on your device
- **7-year record keeping** -- JSON storage meets Section 75 requirements

## Installation

### Option A: ClawHub (recommended)

```bash
# Install the ClawHub CLI if you haven't already
npm i -g clawhub

# Install the skill
clawhub install kiwi-receipts
```

### Option B: Git clone

```bash
git clone https://github.com/maxazure/kiwi-receipts.git ~/.openclaw/skills/kiwi-receipts
```

### Option C: Manual download

Copy the repository into any supported skill directory:

```bash
# Workspace skills (highest priority)
cp -r kiwi-receipts ~/.openclaw/workspace/skills/kiwi-receipts

# Or managed skills directory
cp -r kiwi-receipts ~/.openclaw/skills/kiwi-receipts
```

You can also register an extra skill directory in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "load": {
      "extraDirs": ["/path/to/your/skills/folder"]
    }
  }
}
```

### Python dependency

The XLSX/CSV report generator requires `openpyxl`. Install it before first use:

```bash
pip install openpyxl
```

## How It Works

### Daily: Capture receipts and income

Send a photo of your receipt to your OpenClaw bot (Telegram or WhatsApp):

```
You: [photo of Bunnings receipt]
Bot: Receipt captured:
     Bunnings Warehouse
     2026-03-19
     $174.00 (GST: $22.70)
     Timber 2x4 x10, Concrete Mix x5
     Category: materials

     Reply to save, or correct any details.
You: save
Bot: Saved. Period total: $1,527.37, 5 receipts.
```

Record sales when you invoice a client:

```
You: income 9775 Bathroom renovation - 42 Rimu St, ABC Homes
Bot: Income recorded:
     Client: ABC Homes
     Description: Bathroom renovation - 42 Rimu St
     Amount: $9,775.00 (GST: $1,274.35)
     Date: 2026-03-19

     Reply to save.
```

### Every two months: File GST

NZ GST is filed every two months. Send `report` to generate the XLSX:

```
You: report
Bot: GST Report: Mar-Apr 2026
     Receipts: 23, Income entries: 8
     Total purchases: $8,420.50
     Total sales: $29,670.00
     GST to pay: $2,773.70
     [Download XLSX]
```

The GST101A sheet is fully auto-filled when you have both receipts and income data:

| Box | Description | Value |
|-----|-------------|-------|
| 5 | Total sales (incl GST) | $29,670.00 (auto-filled from income) |
| 10 | Total GST collected | $3,870.00 (auto-calculated) |
| 11 | Total purchases (incl GST) | $8,420.50 (auto-filled from receipts) |
| 12 | GST credit (Box 11 x 3/23) | $1,098.33 (auto-calculated) |
| 15 | GST to pay | $2,771.67 (auto-calculated) |

Log in to [myIR](https://www.ird.govt.nz/), copy the numbers, submit. Done.

### End of tax year: IR3 income tax

At the end of the tax year (31 March), generate your annual tax summary:

```
You: ir3
Bot: Annual Tax Summary: 2025-2026

     Income (excl GST):    $82,608.70
     Less expenses:       -$49,500.00
     Less depreciation:    -$6,246.50
     Taxable income:       $26,862.20

     Income tax:            $3,608.89
     ACC levy:                $448.60
     Less provisional tax: -$2,943.15
     Tax to pay:            $1,114.34

     Reply "export ir3" for the full XLSX report.
```

### Provisional tax

If your previous year tax exceeded $5,000, the skill calculates your instalments:

```
You: provisional
Bot: Provisional Tax 2026-2027:
     Based on 2025-2026 RIT: $8,409.00
     Uplift (x 1.05): $8,829.45
     Per instalment: $2,943.15

     1st: 28 August 2026
     2nd: 15 January 2027
     3rd: 7 May 2027
```

### Asset depreciation

Track tools, vehicles, and equipment:

```
You: asset add DeWalt circular saw $899
Bot: Asset recorded:
     DeWalt circular saw
     Cost: $899.00 (excl GST)
     Category: Portable power tools
     Depreciation: DV 40% (5 year life)
     Year 1 claim: $359.60
```

### Xero export

Generate a CSV importable into Xero:

```
You: xero export
Bot: Xero CSV exported: 35 transactions (Mar-Apr 2026)
     [Download CSV]
```

Import into Xero: Accounting > Bank Accounts > Import Statement.

## NZ GST Filing Periods

| Period | Due Date |
|--------|----------|
| Jan - Feb | 28 March |
| Mar - Apr | 28 May |
| May - Jun | 28 July |
| Jul - Aug | 28 September |
| Sep - Oct | 28 November |
| Nov - Dec | 15 January |

Special dates: periods ending 31 March are due 7 May. Periods ending 30 November are due 15 January.

## First-Time Setup

```
You: setup
Bot: What is your business name?
You: My Construction Ltd
Bot: What is your GST/IRD number?
You: 12-345-678
Bot: Vehicle business use percentage? (default 80)
You: 80
Bot: Phone business use percentage? (default 70)
You: 70
Bot: Saved.
```

## Commands

### Receipts

| Command | Description |
|---------|-------------|
| Send photo | Capture a receipt |
| `summary` | Current GST period overview |
| `report` | Download GST report (XLSX) |
| `report 2026-03` | Report for a specific period |
| `list` | Show recent receipts |
| `delete last` | Remove last receipt |

### Income

| Command | Description |
|---------|-------------|
| `income 9775 description` | Record a sales invoice |
| `income list` | Show recent income entries |
| `income summary` | Current period income total |

### Assets

| Command | Description |
|---------|-------------|
| `asset add name $cost` | Register a depreciable asset |
| `asset list` | Show assets with current book values |
| `asset dispose name $price` | Record asset disposal |
| `depreciation` | Calculate this year's depreciation |

### Tax

| Command | Description |
|---------|-------------|
| `provisional` | Calculate provisional tax instalments |
| `set last year tax 8409` | Set previous year residual income tax |
| `ir3` or `tax return` | Annual income tax summary |
| `export ir3` | Annual XLSX report with all sheets |

### Export

| Command | Description |
|---------|-------------|
| `xero export` | Generate Xero-importable CSV |

### Setup

| Command | Description |
|---------|-------------|
| `setup` | Configure business details |
| `help` | Show all commands |

## XLSX Report Sheets

The generated XLSX can contain up to 7 sheets:

1. **GST Summary** -- business info, period totals
2. **All Receipts** -- every receipt with date, merchant, category, items, amounts
3. **By Category** -- subtotals by expense category
4. **IRD GST101A** -- official box numbers pre-filled for myIR
5. **Income** -- sales/invoice records (when income data exists)
6. **Depreciation** -- asset depreciation schedule (when assets exist)
7. **IR3 Annual Tax** -- full income tax calculation with bracket breakdown (annual reports)

## Legal Compliance

This skill is built with reference to:

- **Goods and Services Tax Act 1985** (NZ) -- Sections 2, 8, 15, 16, 19F, 20, 51, 75
- **Income Tax Act 2007** (NZ) -- Schedule 1 Part A (tax rates), Subpart EE (depreciation), Part RC (provisional tax), Section DA 1 (deductions)
- **Tax Administration Act 1994** -- record keeping, filing deadlines
- **Taxation (Annual Rates for 2021-22, GST, and Remedial Matters) Act 2022** -- TSI framework (effective 1 April 2023)
- **IRD GST101A form** (2023 revision)
- **IRD General Depreciation Rates IR265** (August 2024)

See the `references/` directory for full compliance documentation:
- [`nz-gst-guide.md`](references/nz-gst-guide.md) -- GST Act citations, TSI thresholds, GST101A box reference
- [`nz-income-tax-guide.md`](references/nz-income-tax-guide.md) -- tax brackets, IR3 structure, provisional tax, deductions
- [`nz-depreciation-rates.md`](references/nz-depreciation-rates.md) -- IRD depreciation rates for builder assets

**Disclaimer:** This tool assists with record-keeping and report generation. It is not a substitute for professional tax advice. Always verify figures with a qualified accountant before filing with IRD.

## File Structure

```
kiwi-receipts/
├── SKILL.md                          # OpenClaw skill definition
├── README.md                         # This file
├── scripts/
│   └── generate_report.py            # XLSX/CSV report generator
└── references/
    ├── nz-gst-guide.md               # GST compliance reference
    ├── nz-income-tax-guide.md         # Income tax reference
    └── nz-depreciation-rates.md       # Depreciation rates reference
```

## Data Storage

All data is stored locally on your machine:

```
~/.openclaw/data/kiwi-receipts/
├── config.json        # Business name, GST number, settings
├── receipts.json      # Purchase receipts
├── income.json        # Sales/invoice records
├── assets.json        # Depreciable assets register
└── tax-history.json   # Previous years' tax figures
```

No data is uploaded to any external server by this skill. Receipt image recognition uses the same AI model you have configured in your OpenClaw instance. The skill itself does not call any external API.

## Privacy

- **All data** stored only in `~/.openclaw/data/kiwi-receipts/` on your device
- **Vision processing** uses your OpenClaw model, not a separate service
- **No telemetry** -- this skill does not collect, transmit, or log any usage data
- **No network calls** -- the skill itself makes zero outbound requests

## License

MIT
