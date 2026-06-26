# Nex Expenses

Receipt & Expense Categorizer with Belgian Tax Buckets

Track business expenses with automatic Belgian tax categorization. OCR receipts, auto-categorize into Belgian deduction categories (beroepskosten, representatie 50%, autokosten), generate quarterly summaries for your boekhouder, and track BTW for aangifte.

Built for eenmanszaken (sole traders) and kleine ondernemingen (small businesses) in Belgium.

## Features

- **OCR Receipt Scanning**: Extract vendor, date, and amount automatically from receipt images
- **Natural Language Parsing**: Add expenses in plain Dutch or English (e.g., "lunch bij De Vitrine 45.50 BTW 21%")
- **Auto-Categorization**: Intelligent suggestion of Belgian tax categories based on vendor
- **Belgian Tax Categories**: Full support for all standard tax deduction categories:
  - Beroepskosten (100% deductible)
  - Representatiekosten (50% deductible)
  - Autokosten (variable deductibility)
  - Kantoorkosten (office supplies, 100%)
  - Telecom (100% or 75%)
  - Opleiding (training, 100%)
  - Verzekeringen (insurance, 100%)
  - Huur (office rent, 100%)
  - And more...

- **BTW Tracking**: Automatically track input VAT for quarterly aangifte filing
- **Quarterly Summaries**: Generate financial summaries ready to send to your boekhouder
- **Full-Text Search**: Find expenses by vendor, description, or notes
- **Export for Accountant**: CSV and JSON exports with professional column headers
- **Privacy-First**: All data stays on your machine. No cloud, no tracking.

## Installation

```bash
bash setup.sh
```

This script:
1. Checks for Python 3
2. Creates a virtual environment
3. Installs dependencies (including optional PIL for image preprocessing)
4. Initializes the SQLite database
5. Creates the `nex-expenses` CLI command
6. Checks for tesseract and provides installation instructions if needed

## Quick Start

### Add an expense from a receipt

```bash
nex-expenses add --receipt ~/Pictures/receipt.jpg
```

### Add an expense with natural language

```bash
nex-expenses add "Shell tanken 65,30 21% BTW"
nex-expenses add "lunch bij De Vitrine 45.50 BTW 21%"
```

### Add an expense manually

```bash
nex-expenses add --vendor "Adobe" --amount 15.99 --btw 21 --category kantoorkosten_100
```

### List expenses

```bash
nex-expenses list
nex-expenses list --quarter Q1 --year 2026
nex-expenses list --category representatie_50
```

### Generate quarterly summary

```bash
nex-expenses summary quarterly Q1 2026
```

### Export for accountant

```bash
nex-expenses export csv Q1 2026
```

## Data Storage

All data is stored locally:

- **Database**: `~/.nex-expenses/expenses.db` (SQLite)
- **Receipts**: `~/.nex-expenses/receipts/` (image files stored here)
- **Exports**: `~/.nex-expenses/exports/` (CSV/JSON files)
- **Config**: `~/.nex-expenses/config.json` (user settings)

## Documentation

For complete documentation, see `SKILL.md` or run:

```bash
nex-expenses categories
nex-expenses config show
```

## Requirements

- Python 3.9+
- Tesseract OCR (optional, for receipt scanning)
  - Linux: `sudo apt-get install tesseract-ocr`
  - macOS: `brew install tesseract`
  - Windows: https://github.com/UB-Mannheim/tesseract/wiki

## Supported Image Formats for OCR

- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)
- PDF (.pdf)

## Belgian Tax Information

This tool is built specifically for Belgian tax law. It implements the standard deduction percentages as of 2026:

- Beroepskosten: 100% deductible
- Representatie: 50% deductible
- Autokosten (fuel): 75% deductible
- Home office: typically 20% deductible
- And more...

Always verify with your boekhouder for your specific situation, as some categories may vary based on business type or circumstances.

## Privacy

No data is sent to external servers. All processing happens locally on your machine. Receipt images are stored in your data directory for future reference but can be deleted manually.

## License

MIT-0 (Public Domain Equivalent)

Copyright 2026 Nex AI (Kevin Blancaflor)

## Support

Built by Nex AI - Digital transformation for Belgian SMEs
https://nex-ai.be

## Changelog

### 1.0.0 (2026-04-05)
- Initial release
- OCR receipt scanning with Tesseract
- Natural language expense parsing
- 14+ Belgian tax categories
- Quarterly and yearly summaries
- BTW tracking for aangifte
- Full-text search
- CSV and JSON export
- Vendor auto-categorization
