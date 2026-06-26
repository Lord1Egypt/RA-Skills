---
name: nex-expenses
description: Track and categorize all business expenses with automatic Belgian tax deduction rules and VAT recovery optimization. Use optical character recognition (OCR) with Tesseract to scan receipt images and automatically extract vendor names, transaction amounts, dates, and BTW rates from physical receipt photographs. Intelligently categorize expenses into Belgian tax deduction categories (beroepskosten 100%, representatie 50%, autokosten with fuel/other subcategories, kantoorkosten 100%, kledij/werkkledij, verzekeringen, opleiding, telecom, huurkantoor, etc.) with automatic deductible portion calculation per category following Belgian tax regulations. Generate quarterly summaries organized by tax category with total amounts, deductible amounts, effective deduction percentages, and BTW collected for convenient filing with your boekhouder (accountant). Track input VAT (BTW inkomsten) separately by rate (21%, 12%, 6%, 0%) for quarterly aangifte submissions and maintain complete payment method records (cash, bank transfer, credit card, debit card, cheque). Create professional CSV/JSON exports with Belgian-friendly column headers for import into accounting software. Ideal for freelancers, eenmanszaken, and kleine ondernemingen who need to manage expenses, optimize tax deductions, prepare quarterly accounting documents, and stay compliant with Belgian tax law. All expense data remains local.
version: 1.0.0
metadata:
  clawdbot:
    emoji: "\U0001F9FE"
    requires:
      bins:
        - python3
        - tesseract
      env: []
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-expenses.py"
      - "lib/*"
      - "setup.sh"
---

# Nex Expenses

Track business expenses with automatic Belgian tax categorization. OCR receipts, auto-categorize into Belgian deduction categories, generate quarterly summaries for your boekhouder, and track BTW for aangifte. All data stays on your machine.

## When to Use

Use this skill when the user needs to:

- Add a business expense (receipt, invoice, or manual entry)
- Scan receipts and automatically extract vendor, date, and amount via OCR
- Categorize expenses using Belgian tax deduction rules (beroepskosten, representatie, autokosten, etc.)
- Track BTW (input VAT) for quarterly aangifte filings
- Generate quarterly expense summaries for their boekhouder (accountant)
- Search or list expenses by vendor, category, date, or tag
- Export expenses in CSV or JSON for accounting software
- View category breakdowns and top vendors by spending
- Calculate deductible amounts per expense based on Belgian tax law

Trigger phrases: "add expense", "scan receipt", "business expense", "tax category", "quarterly summary", "export for accountant", "BTW aangifte", "deductible amount", "boekhouder", "representatie", "beroepskosten"

## Quick Setup

If the database does not exist yet, run the setup script:

```bash
bash setup.sh
```

This creates the data directory, installs dependencies in a virtual environment, initializes the database, and creates the CLI wrapper script.

## Available Commands

The CLI tool is `nex-expenses`. All commands output plain text with consistent formatting.

### Add Expense

Three modes for adding expenses:

**Mode 1: Scan Receipt (OCR)**
```bash
nex-expenses add --receipt /path/to/receipt.jpg
nex-expenses add --receipt ~/Downloads/bonnetje.png
```
Automatically extracts vendor, date, amount, and BTW rate from the receipt image. Suggests a category based on vendor recognition.

**Mode 2: Manual Entry with Flags**
```bash
nex-expenses add --vendor "Shell" --amount 65.30 --btw 21 --category autokosten_brandstof --date 2026-04-03
nex-expenses add --vendor "Adobe" --amount 15.99 --btw 21 --category kantoorkosten_100
nex-expenses add --vendor "Restaurant De Vita" --amount 45.50 --btw 21 --category representatie_50 --description "Lunch with client A"
```

**Mode 3: Natural Language (Dutch/English)**
```bash
nex-expenses add "lunch bij De Vitrine 45.50 BTW 21%"
nex-expenses add "Shell tanken 65,30 21% VAT"
nex-expenses add "Adobe subscription 15,99 no BTW"
```
Parses vendor, amount, and BTW rate from free-form text. Auto-categorizes based on vendor.

Common flags for all modes:
- `--category`: Belgian tax category (see `nex-expenses categories`)
- `--date`: Date in YYYY-MM-DD format (default: today)
- `--description`: Additional description
- `--payment-method`: cash, bank_transfer, credit_card, debit_card, cheque
- `--notes`: Internal notes

### List Expenses

View your recorded expenses with various filters:

```bash
nex-expenses list
nex-expenses list --quarter Q1 --year 2026
nex-expenses list --category representatie_50
nex-expenses list --vendor "Shell"
nex-expenses list --since 2026-01-01 --until 2026-03-31
nex-expenses list --tag "project-echo"
nex-expenses list --limit 50
nex-expenses list --output json
```

Filters:
- `--quarter`: Q1, Q2, Q3, or Q4 (with --year)
- `--year`: Year (e.g., 2026)
- `--category`: Tax category ID
- `--vendor`: Vendor name
- `--since` / `--until`: Date range (YYYY-MM-DD)
- `--tag`: Filter by tag
- `--limit`: Max results (default: 100)
- `--output`: text (default) or json

### Show Single Expense

Display full details of an expense by ID:

```bash
nex-expenses show 42
```

Shows date, vendor, amounts, BTW, deductible percentage, and category.

### Edit Expense

Modify an existing expense:

```bash
nex-expenses edit 42 --category kantoorkosten_100
nex-expenses edit 42 --amount 55.00 --btw 21
nex-expenses edit 42 --vendor "Updated Vendor" --description "Corrected description"
```

Automatically recalculates BTW amounts and deductible portions when you change amount or category.

### Delete Expense

Remove an expense from the database:

```bash
nex-expenses delete 42
nex-expenses delete 42 --force
```

Prompts for confirmation unless `--force` is used.

### Search Expenses

Full-text search across vendor names, descriptions, and notes:

```bash
nex-expenses search "Adobe"
nex-expenses search "Shell fuel July"
nex-expenses search "client meeting" --limit 50
```

### Summary Commands

Generate financial summaries for different time periods:

```bash
nex-expenses summary quarterly Q1 2026
nex-expenses summary yearly 2026
nex-expenses summary monthly 2026-04
nex-expenses summary categories --year 2026
nex-expenses summary vendors --top 20
nex-expenses summary btw Q1 2026
```

**Quarterly Summary:** Lists all expenses by category with totals, deductible amounts, and BTW reclaimable.

**Yearly Summary:** Aggregates all quarters, shows category and quarterly breakdowns.

**Monthly Summary:** Expenses for a specific month (format: YYYY-MM).

**Categories:** Breakdown of total spending by tax category for a year.

**Vendors:** Top N vendors by total spending.

**BTW Summary:** Input VAT grouped by rate for BTW-aangifte filing.

### Export for Accountant

Export expenses in formats your boekhouder can import:

```bash
nex-expenses export csv Q1 2026
nex-expenses export csv 2026
nex-expenses export json 2026
```

Generates files in `~/.nex-expenses/exports/` with Belgian-friendly column headers:
- Datum
- Leverancier
- Omschrijving
- Bedrag incl. BTW
- Bedrag excl. BTW
- BTW bedrag
- BTW%
- Categorie
- Aftrekbaar%
- Aftrekbaar bedrag
- Betaalwijze
- Notities

### List Available Categories

View all Belgian tax deduction categories:

```bash
nex-expenses categories
```

Shows category ID, name, deduction percentage, and description for each category.

### Test OCR on Receipt

Debug OCR results without saving:

```bash
nex-expenses ocr /path/to/receipt.jpg
```

Displays vendor, date, amounts, BTW rate, confidence score, detected items, and raw OCR text.

### Overall Statistics

View aggregate statistics:

```bash
nex-expenses stats
nex-expenses stats --year 2026
```

Shows total expenses, total deductible amount, total BTW, and expense count.

### Configuration

Manage configuration settings:

```bash
nex-expenses config show
nex-expenses config set-btw-status vrijgesteld
nex-expenses config set-btw-status plichtig
```

- `show`: Display current configuration
- `set-btw-status`: Mark yourself as BTW-exempt (vrijgesteld) or VAT-liable (plichtig)

## Example Interactions

**User:** "I just bought lunch with a client. It was 45.50 euros including 21% VAT at De Vitrine."
**Agent runs:** `nex-expenses add "lunch bij De Vitrine 45.50 BTW 21%"`
**Agent:** Shows the parsed expense, suggests representatie_50 category, confirms it was saved.

**User:** "Ik heb net getankt bij Shell voor 65 euro."
**Agent runs:** `nex-expenses add "Shell tanken 65 euro"`
**Agent:** Parses vendor and amount, suggests autokosten_brandstof category with high confidence.

**User:** "Hoeveel heb ik dit kwartaal aan representatiekosten uitgegeven?"
**Agent runs:** `nex-expenses summary categories --year 2026` or filters by category
**Agent:** Shows total representatie_50 expenses with deductible portion.

**User:** "Scan dit bonnetje en voeg het toe."
**Agent runs:** `nex-expenses add --receipt /path/to/receipt.jpg`
**Agent:** Performs OCR, shows extracted data, suggests category, saves expense.

**User:** "Exporteer Q1 voor mijn boekhouder."
**Agent runs:** `nex-expenses export csv Q1 2026`
**Agent:** Exports to CSV with professional accounting headers and confirms the file location.

**User:** "Hoeveel BTW kan ik terugvorderen dit kwartaal?"
**Agent runs:** `nex-expenses summary btw Q1 2026`
**Agent:** Shows total reclaimable BTW grouped by rate (21%, 6%, 0%) for aangifte filing.

**User:** "Wat waren mijn top 10 meeste bezochte restaurants?"
**Agent runs:** `nex-expenses summary vendors --top 10` (or filtered by category)
**Agent:** Lists top vendors by spending, showing total amount spent at each.

**User:** "Hoeveel gaf ik uit aan kantoorbenodigdheden vorig maand?"
**Agent runs:** `nex-expenses list --category kantoorkosten_100 --month 2026-03` (or summary monthly)
**Agent:** Shows all kantoorkosten expenses for March 2026 with total.

**User:** "I need to correct expense ID 42. It should be 55 euros not 50."
**Agent runs:** `nex-expenses edit 42 --amount 55.00`
**Agent:** Updates the expense, recalculates BTW and deductible amount automatically.

**User:** "Search for all Adobe expenses."
**Agent runs:** `nex-expenses search "Adobe"`
**Agent:** Lists all matching expenses with IDs, dates, and amounts.

## Output Parsing

All CLI output is plain text, structured for easy parsing:

- Section headers followed by `---` separators
- Currency formatted as €12,34 (with comma as decimal)
- Percentages shown as 21% or 50%
- Amounts are always shown with two decimal places
- ID references formatted as `ID 42` for easy extraction
- Every command output ends with `[Nex Expenses by Nex AI | nex-ai.be]`

When presenting output to the user, strip the footer line and present the information naturally in Dutch or English depending on the context.

## Important Notes on Belgian Tax Rules

- **Beroepskosten (100%)**: General professional expenses fully deductible (office supplies, software, internet, etc.)
- **Representatiekosten (50%)**: Entertainment, restaurants, client gifts - only 50% deductible
- **Autokosten**: Vehicle-related expenses - varies:
  - Brandstofkosten (Fuel): 75% deductible
  - Andere autokosten: 50-120% depending on CO2 emissions
- **Kledij (0%)**: Regular clothing is NOT deductible
- **Werkkledij (100%)**: Work uniforms or safety gear - fully deductible
- **Verzekeringen (100%)**: Professional insurance - fully deductible
- **Opleiding (100%)**: Training, courses, professional development books - fully deductible
- **Huur kantoor (100%)**: Office rent - fully deductible
- **Thuiskantoor (20%)**: Home office portion - typically 20% of rent/mortgage
- **Telecom (100% or 75%)**: Phone/internet fully deductible if 100% professional use, otherwise 75% if mixed use
- **Niet aftrekbaar (0%)**: Personal expenses, groceries, etc. - not deductible

All expenses include calculated deductible amounts based on these percentages. Always verify with your boekhouder for edge cases.

## BTW (VAT) Notes

- Input BTW is tracked separately from deductible amounts
- BTW is on the expense amount BEFORE deduction percentage is applied
- For aangifte quarterly filing, use `nex-expenses summary btw Q1 2026` to get totals by rate
- If you're BTW-exempt (kleine onderneming), use `nex-expenses config set-btw-status vrijgesteld`
- Default assumption is 21% BTW unless specified otherwise

## Data Privacy

All expense data is stored locally at `~/.nex-expenses/`. No telemetry, no analytics. No external API calls are made unless you explicitly configure them. OCR via Tesseract runs locally on your machine.

## Troubleshooting

- **"Tesseract not installed"**: Install tesseract-ocr:
  - Linux: `sudo apt-get install tesseract-ocr`
  - macOS: `brew install tesseract`
  - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
- **"Database not found"**: Run `bash setup.sh` to initialize
- **"OCR gives poor results"**: Try improving image quality, ensure receipt text is clearly visible and not at an angle
- **"Category not found"**: Run `nex-expenses categories` to see all available categories
- **"Amount parsing failed"**: Use explicit flags like `--vendor "X" --amount 50.00 --btw 21` instead of natural language

## Expenses Directory

- **Data**: `~/.nex-expenses/expenses.db`
- **Receipts**: `~/.nex-expenses/receipts/` (receipt images are stored here)
- **Exports**: `~/.nex-expenses/exports/` (generated CSV/JSON files)
- **Config**: `~/.nex-expenses/config.json` (user settings)

## Credits

Built by Nex AI (https://nex-ai.be) - Digital transformation for Belgian SMEs and freelancers.
Author: Kevin Blancaflor
License: MIT-0
