# Home Inventory

Document everything you own for **insurance**, **moving**, or **estate planning**.

A lightweight, dependency-free Python tool that manages a JSON database of household items with depreciation tracking, insurance-ready reports, and a moving box labeling system.

## Features

- 📦 **Item Management** — Add, list, search, and categorize household items
- 💰 **Depreciation Tracking** — Category-aware depreciation (electronics depreciate fast, jewelry appreciates)
- 🏠 **Insurance Reports** — Replacement cost summaries, room-by-room breakdowns, high-value flags
- 📦 **Moving Box System** — Assign items to boxes, generate QR-friendly manifests
- 📊 **CSV Export** — Export to spreadsheets or upload to insurance providers
- 🔒 **100% Local** — Your data stays in a local JSON file. No cloud, no accounts.

## Quick Start

```bash
# Add an item
python scripts/inventory.py add \
  --name "MacBook Pro" --category electronics --room office \
  --value 2400 --brand "Apple" --model "MBP 14 M3" \
  --serial "C02XK1234ABC" --purchase-date 2024-03-15

# See everything
python scripts/inventory.py list

# Insurance report
python scripts/inventory.py insurance-report

# Depreciation report
python scripts/inventory.py depreciation-report

# Export to CSV
python scripts/inventory.py export-csv --output my_inventory.csv

# Moving boxes
python scripts/inventory.py assign-box --item-id 1 --box BOX-001
python scripts/inventory.py box-manifest BOX-001
```

## Requirements

- Python 3.8+ (stdlib only — no pip dependencies)

## Commands

| Command              | Description                                    |
|----------------------|------------------------------------------------|
| `add`                | Add a new item                                 |
| `list`               | List all items                                 |
| `search`             | Search items by keyword                        |
| `by-room`            | Filter items by room                           |
| `total-value`        | Show total value of all items                  |
| `export-csv`         | Export inventory to CSV                        |
| `insurance-report`   | Generate insurance-ready report                |
| `depreciation-report`| Show depreciation by category                  |
| `assign-box`         | Assign an item to a moving box                 |
| `box-manifest`       | Generate a QR-friendly box manifest            |

## Project Structure

```
home-inventory/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── inventory.py
└── references/
    ├── insurance-claims-guide.md
    └── depreciation-tables.md
```

## License

MIT © Denis Voronin
