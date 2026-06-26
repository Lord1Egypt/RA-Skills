# Nex E-Invoice

**Generate Belgian-compliant UBL e-invoices (Peppol BIS 3.0) from natural language.**

Built by **Nex AI** - Digital transformation for Belgian SMEs.

## What It Does

- Create professional invoices from natural language input in Dutch or English
- Automatically calculate VAT/BTW using correct Belgian rates (0%, 6%, 12%, 21%)
- Generate Peppol BIS 3.0 compliant UBL XML invoices (mandatory for B2B from January 2026)
- Manage customer contacts with automatic VAT-ID validation
- Track invoice status (draft, sent, paid, overdue) with payment notes
- Create credit notes for returns and adjustments
- Generate statistics on invoiced amounts, outstanding payments, and VAT collected
- Export invoices as XML for accounting systems, e-banking, and tax compliance
- All invoice data stays local on your machine. No telemetry. You own your data.

## Quick Install

```bash
# Via ClawHub
clawhub install nex-einvoice

# Or manual
git clone <repo-url>
cd nex-einvoice
bash setup.sh
```

## Example Usage

Ask your AI agent to create invoices and manage billing:

```
You: Factureer Bakkerij Peeters voor 3 broodjes aan 2.50 euro, BTW 6%
Agent: Creating invoice...
       Invoice INV-2026-0001
       Customer: Bakkerij Peeters
       3x Broodjes @ EUR 2.50 = EUR 7.50
       VAT (6%): EUR 0.45
       Total: EUR 7.95

You: Maak een factuur voor ECHO Management: 5 uur consulting aan 95 euro per uur
Agent: Creating invoice...
       Invoice INV-2026-0002
       Customer: ECHO Management
       5h Consulting @ EUR 95.00 = EUR 475.00
       VAT (21%): EUR 99.75
       Total: EUR 574.75

You: Welke facturen staan nog open?
Agent: Open invoices:
       - INV-2026-0001 Bakkerij Peeters EUR 7.95 (draft)
       - INV-2026-0002 ECHO Management EUR 574.75 (sent)

You: Markeer INV-2026-0001 als betaald
Agent: Invoice INV-2026-0001 marked as paid on 2026-04-05.

You: Hoeveel heb ik deze maand gefactureerd?
Agent: April 2026 statistics:
       Total invoiced: EUR 582.70
       Number of invoices: 2
       Average invoice: EUR 291.35
       Outstanding: EUR 0.00

You: Voeg Watt's Smart BV toe met BTW BE0987654321
Agent: Contact added:
       Name: Watt's Smart BV
       VAT-ID: BE0987654321
       Ready for invoicing.

You: Exporteer INV-2026-0002 als XML
Agent: Exported to invoice.xml (Peppol BIS 3.0 compliant)
```

## Configuration

After installation, configure your company details for seller information on invoices:

```bash
# Set seller company information
nex-einvoice config set-seller \
  --name "Your Company Name" \
  --address "Street 123" \
  --city "Antwerp" \
  --postal "2000" \
  --country "BE" \
  --vat-id "BE0123456789" \
  --email "invoices@yourcompany.be"

# Set payment details for invoices
nex-einvoice config set-payment \
  --terms "NET30" \
  --iban "BE89 3200 1234 5678" \
  --bic "GEBABEBB" \
  --bank-name "ING Belgium"

# Set invoice number prefix
nex-einvoice config set-prefix "INV-2026"

# View current configuration
nex-einvoice config show
```

## Belgian E-Invoicing Context

The Belgian government mandates e-invoicing for all B2B transactions starting January 2026. Nex E-Invoice generates fully compliant Peppol BIS 3.0 UBL invoices that meet all legal requirements:

- Unique sequential invoice numbering per fiscal year
- Mandatory VAT identification for both parties
- Peppol network compatibility (exchange via electronic data interchange)
- Automatic validation against Belgian accounting rules
- Support for payment terms and structured payment references
- Compliance with EN 16931 European standard

## Supported Features

- **Natural Language**: Create invoices in Dutch or English by describing them conversationally
- **Flexible Input**: Structured command-line format or JSON for programmatic use
- **VAT Calculation**: Automatic, correct application of Belgian VAT rates
- **Contact Management**: Store and reuse customer information with VAT validation
- **Status Tracking**: Draft, sent, paid, overdue with payment date recording
- **Credit Notes**: Create refund/adjustment notes linked to original invoices
- **Search**: Full-text search across all invoice data
- **Statistics**: Aggregated views by period, customer, or payment status
- **XML Export**: Peppol BIS 3.0 UBL format for accounting integration
- **Validation**: Automatic compliance checking against Belgian e-invoicing rules

## Privacy

Nex E-Invoice is built privacy-first:

- All invoice data is stored locally in `~/.einvoice/` on your machine
- No external API calls are made (VAT-ID validation is cached locally)
- No telemetry, no analytics, no tracking of any kind
- No external servers: all processing is local
- Customer data is encrypted in the local database
- Export files are your property—stored and controlled only by you

## How It Works

1. **Input Processing**: Natural language descriptions are parsed by the local NLP engine to extract invoice details (customer, items, quantities, prices, VAT rates).

2. **VAT Calculation**: Amounts are calculated with proper Belgian VAT application and rounding (2 decimal places).

3. **Storage**: Invoice data is stored in a local SQLite database with full audit trail (creation date, modifications, payment status).

4. **Export**: Invoices can be exported as human-readable text, PDF, or Peppol BIS 3.0 compliant UBL XML.

5. **Contact Management**: Customer information is validated (VAT-ID format check) and cached for reuse across invoices.

6. **Compliance**: All invoices are automatically validated against Belgian e-invoicing requirements before export.

## CLI Reference

```
nex-einvoice create <text>            Create invoice from natural language
nex-einvoice create --structured      Create with explicit fields
nex-einvoice create --json            Create from JSON data
nex-einvoice show <invoice-id>        Display invoice details
nex-einvoice list [options]           List invoices with filters
nex-einvoice search <query>           Search invoices by content
nex-einvoice status <id> [new-status] View or update payment status
nex-einvoice xml <invoice-id>         Export as Peppol BIS 3.0 UBL XML
nex-einvoice contact add              Add customer contact
nex-einvoice contact show             Display contact details
nex-einvoice contact list             List all contacts
nex-einvoice stats [options]          View invoice statistics
nex-einvoice validate <invoice-id>    Validate against Belgian rules
nex-einvoice config show              View settings
nex-einvoice config set-seller        Set company information
nex-einvoice config set-payment       Set payment details
nex-einvoice config set-prefix        Set invoice number prefix
```

See SKILL.md for full command documentation and examples.

## Credits

- **Built by**: Nex AI (https://nex-ai.be)
- **Author**: Kevin Blancaflor
- **License**: MIT-0

## License

MIT No Attribution (MIT-0). See [LICENSE](LICENSE) for details.
