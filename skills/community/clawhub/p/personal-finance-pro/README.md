# personal-finance

Parse, categorize, and report on personal finance CSV exports — offline, secure, and scriptable.

## Purpose

Process bank and credit card transaction CSVs locally without external API calls or cloud uploads. Validate schema, categorize transactions using keyword rules, and generate spending reports with automatic account number masking for privacy.

## Features

- **Offline-only**: All processing happens locally using bash and jq
- **Privacy-first**: Automatically masks account numbers (shows last 4 digits only)
- **Flexible categorization**: Keyword-based rules via JSON config
- **Multiple reports**: Validate, summarize by period, categorize, and generate insights
- **Safe by default**: Read-only unless you explicitly specify `--output`

## Installation

```bash
# Clone the repository
git clone https://github.com/ppopen/personal-finance.git
cd personal-finance

# Make the script executable (if needed)
chmod +x personal-finance.sh

# Verify installation with sample data
./personal-finance.sh validate
```

## Usage

All commands follow this pattern:

```bash
./personal-finance.sh <command> [--csv <path>] [--config <path>] [--output <path>] [--period <period>]
```

### Commands

#### validate

Check CSV schema and data integrity:

```bash
./personal-finance.sh validate --csv sample-data/sample-transactions.csv
```

Verifies required fields (`date`, `description`, `amount`, `account_number`) and numeric amounts.

#### summarize

Aggregate income and expenses by time period:

```bash
./personal-finance.sh summarize --period month --csv sample-data/sample-transactions.csv
```

Periods: `month` (default), `quarter`, or `year`

#### categorize

Apply keyword rules to assign categories:

```bash
# Preview with masked accounts (read-only)
./personal-finance.sh categorize --csv sample-data/sample-transactions.csv

# Write categorized CSV
./personal-finance.sh categorize --csv input.csv --output /tmp/categorized.csv
```

#### report

Generate spending insights:

```bash
./personal-finance.sh report --csv sample-data/sample-transactions.csv
```

Shows top merchants, categories by spend, and transaction counts.

## Configuration

### Category Rules

Edit `config/category-rules.json` to customize categorization:

```json
{
  "categories": {
    "groceries": ["whole foods", "safeway", "trader joe"],
    "dining": ["restaurant", "cafe", "starbucks"],
    "transport": ["uber", "lyft", "gas station"]
  }
}
```

The script matches transaction descriptions against these keywords (case-insensitive).

### Sample Data

`sample-data/sample-transactions.csv` provides a minimal example:

```csv
date,description,merchant,category,amount,account_number
2024-01-15,Coffee Shop,Local Cafe,dining,-4.50,1234567890
```

Required fields: `date`, `description`, `amount`, `account_number`

## Security & Privacy

- **No network calls**: All processing is local
- **Account masking**: Outputs show `******1234` instead of full account numbers
- **Safe output paths**: Script validates output paths to prevent overwrites
- **File size limits**: Designed for typical personal finance CSVs (tested up to 50K transactions)
- **Read-only by default**: No files modified unless you specify `--output`

## Requirements

- bash 4.0+
- jq (for JSON processing)

## License

MIT License - see LICENSE file for details
