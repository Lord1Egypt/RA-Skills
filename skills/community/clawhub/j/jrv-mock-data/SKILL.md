---
name: jrv-mock-data
description: Generate realistic fake/mock data for testing and development. Supports names, emails, addresses, phone numbers, UUIDs, dates, lorem ipsum, credit cards, companies, and more. Output as JSON, CSV, or SQL INSERT statements.
---

# jrv-mock-data

Generate realistic test data instantly — no API key, no network. Supports dozens of data types, bulk generation, and multiple output formats including JSON, CSV, and SQL.

## Quick Start

```bash
# Generate 10 fake users as JSON
python3 scripts/mock_data.py user --count 10

# Generate fake email addresses
python3 scripts/mock_data.py email --count 5

# Generate addresses
python3 scripts/mock_data.py address --count 3

# Generate a custom record with multiple fields
python3 scripts/mock_data.py record --fields "name,email,phone,company" --count 5

# Output as CSV
python3 scripts/mock_data.py user --count 20 --format csv

# Output as SQL INSERT
python3 scripts/mock_data.py user --count 10 --format sql --table users

# Single values (no count)
python3 scripts/mock_data.py uuid
python3 scripts/mock_data.py name
python3 scripts/mock_data.py lorem --words 50

# Save to file
python3 scripts/mock_data.py user --count 100 --format csv --output test_users.csv
```

## Commands & Data Types

| Type | Description | Example Output |
|------|-------------|----------------|
| `user` | Full user record (name, email, phone, address) | `{"name": "Jane Smith", "email": "jane@example.com", ...}` |
| `name` | Full name | `"Marcus Rivera"` |
| `email` | Email address | `"tmarcus@fakecorp.io"` |
| `phone` | US phone number | `"(415) 555-0193"` |
| `address` | Street address | `"1234 Oak Ave, Austin TX 78701"` |
| `company` | Company name | `"Nexigen Solutions LLC"` |
| `uuid` | UUID v4 | `"f47ac10b-58cc-..."` |
| `date` | Random date | `"2024-07-15"` |
| `datetime` | Random datetime | `"2024-07-15T14:23:00"` |
| `lorem` | Lorem ipsum text | `"Lorem ipsum dolor sit amet..."` |
| `number` | Random integer | `42` |
| `float` | Random float | `3.14159` |
| `bool` | True/false | `true` |
| `color` | Hex color | `"#3a7bd5"` |
| `url` | Fake URL | `"https://fakecorp.io/api/v1"` |
| `ip` | IPv4 address | `"192.168.1.104"` |
| `record` | Custom fields combo | Use `--fields name,email,phone` |

## Formats

| Format | Flag | Notes |
|--------|------|-------|
| JSON | `--format json` (default) | Pretty-printed array |
| CSV | `--format csv` | With header row |
| SQL | `--format sql --table <name>` | INSERT statements |
| Lines | `--format lines` | One value per line |

## Options

| Flag | Description |
|------|-------------|
| `--count N` | Number of records (default: 1) |
| `--format <fmt>` | Output format: json, csv, sql, lines |
| `--table <name>` | Table name for SQL output |
| `--fields <list>` | Comma-separated fields for `record` type |
| `--seed N` | Random seed for reproducible output |
| `--output <file>` | Write to file instead of stdout |

## Use Cases

- **API testing**: Seed databases with realistic-looking test records
- **UI prototyping**: Fill mockups with plausible names and emails
- **QA automation**: Generate test fixtures in CSV or JSON
- **SQL seeding**: Ready-to-paste INSERT statements for dev databases
- **Load testing**: Generate thousands of unique records instantly
