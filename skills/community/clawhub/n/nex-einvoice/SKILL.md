---
name: nex-einvoice
description: Generate Belgian-compliant e-invoices in the Peppol BIS 3.0 UBL format from natural language input in Dutch or English, satisfying mandatory requirements for Belgian B2B invoicing from January 2026 onwards. Create professional invoices directly from conversational descriptions (e.g., "invoice ECHO Management for 5 hours consulting at 95 euros with 21% VAT"). Automatically calculate BTW (Belgian VAT) at correct rates (0%, 6%, 12%, 21%), manage comprehensive customer contact databases with VAT-ID validation against EU VIES, configure seller company information and payment defaults. Track invoice status through complete lifecycle (draft, sent, paid, overdue) with automatic payment date logging and reminders. Export invoices as standardized XML in Peppol BIS 3.0 format for seamless integration with accounting software, e-banking systems, and compliance tools. Supports structured payment references (betaalreferentie), automatic sequential invoice numbering per fiscal year, flexible payment terms (NET30, NET45, etc.), and credit note generation for returns or corrections. View comprehensive statistics on invoiced amounts, outstanding balances, customer breakdowns, and VAT collected for quarterly aangifte filing. Ideal for freelancers, eenmanszaken, and small Belgian SMEs who invoice regularly. All invoice data encrypted and stored locally.
version: 1.0.0
metadata:
  clawdbot:
    emoji: "\U0001F9FE"
    requires:
      bins:
        - python3
      env: []
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-einvoice.py"
      - "lib/*"
      - "setup.sh"
      - "templates/*"
---

# Nex E-Invoice

Generate Belgian-compliant UBL e-invoices (Peppol BIS 3.0) from natural language. Supports Dutch and English input with automatic BTW calculation, structured payment references, contact management, and invoice tracking.

## When to Use

Use this skill when the user asks about:

- Creating invoices or facturen in Dutch or English
- Calculating BTW (Belgian VAT) automatically
- Generating e-invoices compliant with Peppol BIS 3.0 standard
- Managing customer contacts and company information
- Tracking invoice status (draft, sent, paid, overdue)
- Creating credit notes (credit memos, creditnota's)
- Searching for invoices by customer name, reference, or date
- Exporting invoices as XML/UBL for e-banking or accounting systems
- Viewing invoice history and payment tracking
- Statistics on invoiced amounts, outstanding payments, BTW collected
- Validating invoice data against Belgian e-invoicing rules
- Setting payment terms, references, and structured payment info

Trigger phrases: "maak een factuur", "invoice", "factuur", "BTW berekenen", "credit note", "creditnota", "e-invoice", "Peppol", "UBL", "facturatie", "betaalreferentie", "invoice status", "klantenlijst", "contact toevoegen"

## Quick Setup

If the database does not exist yet, run the setup script:

```bash
bash setup.sh
```

This creates the data directory, installs dependencies in a virtual environment, initializes the invoice database, and optionally loads default company seller information.

## Available Commands

The CLI tool is `nex-einvoice`. All commands output plain text or XML as specified.

### Create Invoice

Create new invoices from natural language, structured data, or JSON:

```bash
# Natural language (Dutch or English)
nex-einvoice create "Factureer Bakkerij Peeters voor 3 broodjes aan 2.50 euro, BTW 6%"
nex-einvoice create "Invoice ECHO Management: 5 uur consulting aan 95 euro per uur, 21% VAT"

# Structured format
nex-einvoice create --structured \
  --customer "Bakkerij Peeters" \
  --description "3x Broodjes" \
  --quantity 3 \
  --unit-price 2.50 \
  --vat-rate 6

# JSON format
nex-einvoice create --json '{"customer":"ECHO Management","items":[{"description":"Consulting","quantity":5,"unit_price":95,"vat_rate":21}],"payment_reference":"ECHO-2026-001"}'

# With payment terms
nex-einvoice create --structured \
  --customer "Ribbens Airco" \
  --description "Installatie airco systeem" \
  --unit-price 1500 \
  --vat-rate 21 \
  --payment-terms "NET30"
```

### Show Invoice

Display a specific invoice in human-readable format:

```bash
nex-einvoice show INV-2026-0001
nex-einvoice show INV-2026-0001 --format pdf
nex-einvoice show INV-2026-0001 --format json
```

### List Invoices

List all invoices with filtering options:

```bash
# All invoices
nex-einvoice list

# Filter by status
nex-einvoice list --status draft
nex-einvoice list --status sent
nex-einvoice list --status paid
nex-einvoice list --status overdue

# Filter by date range
nex-einvoice list --since 2026-01-01 --until 2026-03-31
nex-einvoice list --month 2026-03

# Filter by customer
nex-einvoice list --customer "Bakkerij"

# Filter by amount
nex-einvoice list --min-amount 100 --max-amount 5000

# Combine filters
nex-einvoice list --status open --since 2026-01-01
nex-einvoice list --customer "Watt's" --status paid
```

### Search Invoices

Full-text search across invoice data:

```bash
nex-einvoice search "Bakkerij Peeters"
nex-einvoice search "consulting" --customer "ECHO"
nex-einvoice search "airco installation" --since 2026-02-01
nex-einvoice search "sensor" --status paid
```

### Invoice Status

Update or view invoice payment status:

```bash
# View status
nex-einvoice status INV-2026-0001

# Update to sent
nex-einvoice status INV-2026-0001 sent

# Update to paid
nex-einvoice status INV-2026-0001 paid --payment-date 2026-04-05

# Mark as overdue
nex-einvoice status INV-2026-0001 overdue

# Add payment note
nex-einvoice status INV-2026-0001 paid --note "Received via SEPA transfer"
```

### XML/UBL Export

Export invoice as Peppol BIS 3.0 UBL XML:

```bash
nex-einvoice xml INV-2026-0001
nex-einvoice xml INV-2026-0001 --output invoice.xml
nex-einvoice xml INV-2026-0001 --validate
```

### Contact Management

Add, view, and manage customer contacts:

```bash
# Add new contact
nex-einvoice contact add \
  --name "Bakkerij Peeters" \
  --address "Kerkstraat 15" \
  --city "Gent" \
  --postal "9000" \
  --country "BE" \
  --vat-id "BE0123456789" \
  --email "info@bakkerij-peeters.be"

# Show contact
nex-einvoice contact show "Bakkerij Peeters"

# List all contacts
nex-einvoice contact list

# Update contact
nex-einvoice contact update "Bakkerij Peeters" \
  --email "new-email@bakkerij-peeters.be"

# Delete contact
nex-einvoice contact delete "Bakkerij Peeters"
```

### Statistics

View invoice statistics and summaries:

```bash
# Overall stats
nex-einvoice stats

# Stats for a specific period
nex-einvoice stats --month 2026-03
nex-einvoice stats --since 2026-01-01 --until 2026-03-31

# Stats by customer
nex-einvoice stats --customer "Bakkerij Peeters"

# Detailed breakdown
nex-einvoice stats --detail
```

### Validate Invoice

Validate invoice data against Belgian e-invoicing rules:

```bash
nex-einvoice validate INV-2026-0001
nex-einvoice validate --json '{"customer":"Test","items":[{"description":"Service","quantity":1,"unit_price":100,"vat_rate":21}]}'
```

### Configuration

View and set seller (company) information and payment defaults:

```bash
# Show current config
nex-einvoice config show

# Set seller company details
nex-einvoice config set-seller \
  --name "Your Company Name" \
  --address "Street 123" \
  --city "Antwerp" \
  --postal "2000" \
  --country "BE" \
  --vat-id "BE0987654321" \
  --email "invoices@yourcompany.be"

# Set payment defaults
nex-einvoice config set-payment \
  --terms "NET30" \
  --iban "BE89 3200 1234 5678" \
  --bic "GEBABEBB" \
  --bank-name "ING Belgium"

# Set invoice numbering prefix
nex-einvoice config set-prefix "INV-2026"

# Reset to defaults
nex-einvoice config reset
```

## Example Interactions

**User:** "Factureer Bakkerij Peeters voor 3 broodjes aan 2.50 euro, BTW 6%"
**Agent runs:** `nex-einvoice create "Factureer Bakkerij Peeters voor 3 broodjes aan 2.50 euro, BTW 6%"`
**Agent:** Creates and displays the invoice with automatic BTW calculation (7.50 + 0.45 = 7.95 total).

**User:** "Maak een factuur voor ECHO Management: 5 uur consulting aan 95 euro per uur, 21% VAT"
**Agent runs:** `nex-einvoice create "Maak een factuur voor ECHO Management: 5 uur consulting aan 95 euro per uur, 21% VAT"`
**Agent:** Creates invoice for 475 euros with VAT (575 total) and displays invoice number.

**User:** "Welke facturen staan nog open?"
**Agent runs:** `nex-einvoice list --status draft` and `nex-einvoice list --status sent`
**Agent:** Shows all open/unsent invoices with customer names, amounts, and dates.

**User:** "Hoeveel heb ik dit kwartaal gefactureerd?"
**Agent runs:** `nex-einvoice stats --since 2026-01-01 --until 2026-03-31`
**Agent:** Displays total invoiced amount, number of invoices, and average invoice value for Q1 2026.

**User:** "Markeer factuur INV-2026-0001 als betaald"
**Agent runs:** `nex-einvoice status INV-2026-0001 paid --payment-date 2026-04-05`
**Agent:** Updates invoice status and confirms payment recorded.

**User:** "Toon me de factuur voor Ribbens Airco"
**Agent runs:** `nex-einvoice search "Ribbens Airco"` then `nex-einvoice show [matching-invoice-number]`
**Agent:** Displays the full invoice details for Ribbens Airco with all line items.

**User:** "Genereer een credit nota voor Watt's Smart BV: retour 2x sensor 45 euro"
**Agent runs:** `nex-einvoice create --credit-note "Watt's Smart BV" --description "Return 2x sensor" --quantity 2 --unit-price 45 --vat-rate 21`
**Agent:** Creates a credit note reducing Watt's Smart BV invoice balance.

**User:** "Voeg Bakkerij Peeters toe als contact: BTW BE0123456789, Kerkstraat 15 Gent"
**Agent runs:** `nex-einvoice contact add --name "Bakkerij Peeters" --address "Kerkstraat 15" --city "Gent" --vat-id "BE0123456789"`
**Agent:** Adds contact and confirms it can be used for future invoices.

**User:** "Exporteer factuur INV-2026-0001 als XML voor mijn boekhouding"
**Agent runs:** `nex-einvoice xml INV-2026-0001 --output invoice.xml`
**Agent:** Exports invoice in Peppol BIS 3.0 UBL format ready for accounting software.

**User:** "Hoeveel betaalmogelijkheden heb ik ingesteld?"
**Agent runs:** `nex-einvoice config show`
**Agent:** Shows current IBAN, payment terms, and company details.

## Output Parsing

All CLI output is plain text or XML, structured for easy parsing:

- Section headers followed by `---` separators (for text output)
- List items prefixed with `- `
- Invoice line items indented with `  * `
- Currency amounts formatted as EUR with 2 decimal places
- Dates in ISO-8601 format (YYYY-MM-DD)
- Invoice numbers in format `INV-YYYY-NNNN`
- BTW/VAT percentages shown explicitly (e.g., "21% VAT")
- Every command output ends with `[Nex E-Invoice by Nex AI | nex-ai.be]`

When presenting output to the user, strip the footer line and present the information naturally. Format amounts in user's currency preference.

## Important Notes

- All invoice data is stored locally at `~/.einvoice/`. No telemetry, no analytics.
- E-invoices must comply with Peppol BIS 3.0 standard (mandatory for Belgian B2B from January 2026).
- VAT/BTW identification numbers (VAT-IDs) are validated against the EU VIES database for correctness.
- Invoice numbering must be sequential within each fiscal year (2026 starts fresh with INV-2026-0001).
- Payment terms follow ISO 20022 standards (NET30, NET45, etc.).
- IBAN/BIC validation is performed according to international banking standards.
- The system automatically detects Dutch vs. English language input and sets invoice language accordingly.
- Credit notes are tracked separately but share the same invoice number sequence with an appended "CN" suffix.
- All amounts are calculated with proper rounding (2 decimal places) following Belgian accounting rules.
- Contacts are stored locally and can be reused across multiple invoices to ensure consistency.

## Troubleshooting

- **"Contact not found"**: Check spelling or run `nex-einvoice contact list` to see available contacts.
- **"Invalid VAT-ID"**: Ensure format is correct (e.g., "BE" + 10 digits). Verify with `nex-einvoice validate`.
- **"Database not found"**: Run `bash setup.sh` to initialize the invoice database.
- **"Invoice not found"**: Use `nex-einvoice list` to see all invoices and correct the invoice number.
- **"Invalid IBAN"**: Verify IBAN format and country code match. Run `nex-einvoice config show` to check.
- **"No invoices this month"**: Check date range with `nex-einvoice list --month YYYY-MM`.
- **"XML validation failed"**: Run `nex-einvoice validate [invoice-number]` to see specific errors.
- **"BTW calculation incorrect"**: Ensure VAT rate matches Belgian requirements (0%, 6%, 12%, or 21%).

## Credits

Built by Nex AI (https://nex-ai.be) - Digital transformation for Belgian SMEs.
Author: Kevin Blancaflor
