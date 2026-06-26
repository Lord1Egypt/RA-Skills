---
name: "Invoice Forge Professional Invoice Generator"
description: "Professional invoice generation for freelancers and small businesses. Generate beautiful invoices in seconds. No dependencies, no subscriptions, no cloud required. Clean Python code."
author: "@TheShadowRose"
version: "1.0.0"
tags: ["invoice", "freelance", "billing", "business", "generator", "python"]
license: "MIT"
---

# Invoice Forge Professional Invoice Generator

Professional invoice generation for freelancers and small businesses. Generate beautiful invoices in seconds. No dependencies, no subscriptions, no cloud required. Clean Python code.

---

**Professional invoice generation for freelancers and small businesses.**

Generate beautiful, professional invoices in seconds. No dependencies, no subscriptions, no cloud required. Just clean Python code that works.

Created by **Shadow Rose** • quality-verified • MIT License

---

## What It Does

Invoice Forge helps you:

- **Generate professional invoices** with clean, print-ready HTML templates
- **Manage clients** with a simple database
- **Track payments** and see what's overdue at a glance
- **Calculate taxes and discounts** automatically
- **Create recurring invoices** from templates (monthly retainers, subscriptions)
- **Run reports** on revenue, outstanding balances, and client activity

Perfect for freelancers, consultants, indie creators, and small businesses who need invoicing that just works.

---

## Quick Start

### 1. Set Up Your Configuration

Copy the example config and customize it:

```bash
cp config_example.json config.json
```

Edit `config.json` with your business details:

```python
BUSINESS_NAME = "Acme Consulting"
BUSINESS_EMAIL = "billing@acme.com"
CURRENCY_SYMBOL = "$"
DEFAULT_PAYMENT_TERMS = 30  # Net 30
TAX_RATES = {"sales_tax": 0.08}  # 8% sales tax
```

### 2. Add a Client

```bash
python invoice_clients.py add client001 "John Doe" "john@example.com" "123 Main St, City" "+1-555-0100"
```

### 3. Create an Invoice

```bash
python invoice_forge.py create client001 \
  --item "Web Design Services" 1 2500.00 \
  --item "Hosting Setup" 1 500.00 \
  --terms 30
```

This creates an invoice, saves it as HTML in the `output/` folder, and records it in your ledger.

### 4. View Your Invoices

```bash
# List all invoices
python invoice_forge.py list

# See summary stats
python invoice_report.py summary

# Check for overdue invoices
python invoice_report.py overdue
```

---

## Features

### Client Management

Store client details once, reuse forever:

```bash
# Add a client
python invoice_clients.py add acme "Acme Corp" "billing@acme.com"

# List all clients
python invoice_clients.py list

# Search clients
python invoice_clients.py list "acme"

# Update client info
python invoice_clients.py update acme phone="+1-555-1234"

# Get client details
python invoice_clients.py get acme
```

### Invoice Generation

Create invoices with multiple line items, taxes, and discounts:

```bash
# Basic invoice
python invoice_forge.py create client001 \
  --item "Consulting" 10 150.00 \
  --item "Expenses" 1 250.00

# With discount
python invoice_forge.py create client001 \
  --item "Web Development" 40 125.00 \
  --discount-percent 10

# With custom terms
python invoice_forge.py create client001 \
  --item "Design Work" 1 5000.00 \
  --terms 15 \
  --notes "Thank you for your business!"

# Custom invoice date
python invoice_forge.py create client001 \
  --item "Monthly Retainer" 1 3000.00 \
  --date 2024-01-01
```

### Output Formats

Generate invoices in multiple formats:

```bash
# HTML (default - professional, print-ready)
python invoice_forge.py create client001 --item "Service" 1 1000 --format html

# Markdown (for version control, notes)
python invoice_forge.py create client001 --item "Service" 1 1000 --format markdown

# Plain Text (for email, terminal display)
python invoice_forge.py create client001 --item "Service" 1 1000 --format text
```

### Payment Tracking

Update invoice status as payments come in:

```bash
# Mark as paid
python invoice_forge.py status INV-0001 paid

# Mark as cancelled
python invoice_forge.py status INV-0002 cancelled

# List by status
python invoice_forge.py list --status pending
python invoice_forge.py list --status paid
```

### Recurring Templates

Set up templates for regular invoices:

Edit `config.json`:

```python
RECURRING_TEMPLATES = {
    "monthly_retainer": {
        "items": [
            {"description": "Monthly Retainer", "quantity": 1, "rate": 5000.00}
        ],
        "payment_terms": 15,
        "notes": "Monthly retainer for ongoing services.",
    },
}
```

Then use it:

```bash
python invoice_forge.py template monthly_retainer client001
```

### Reports & Analytics

Get insights into your business:

```bash
# Overall summary
python invoice_report.py summary

# Client-specific summary
python invoice_report.py client client001

# Overdue invoices
python invoice_report.py overdue

# Revenue by month
python invoice_report.py revenue --period month

# Top clients by revenue
python invoice_report.py top --limit 10

# Aging report (who owes what for how long)
python invoice_report.py aging
```

---

## Use Cases

### Freelance Consultants

Track client hours, generate invoices weekly or monthly, monitor who's paid and who hasn't.

```bash
python invoice_forge.py create client001 \
  --item "Strategy Consulting - Week of Jan 15" 20 200.00 \
  --terms 15
```

### Digital Product Sellers

Invoice for one-time purchases, custom work, or licensing fees.

```bash
python invoice_forge.py create client002 \
  --item "Premium License - VideoEdit Pro" 1 499.00 \
  --item "Priority Support (1 year)" 1 99.00
```

### Small Agencies

Manage multiple clients, track monthly retainers, generate reports for accounting.

```bash
# Set up recurring template in config.json
python invoice_forge.py template monthly_retainer agency_client_001
python invoice_forge.py template monthly_retainer agency_client_002

# Review outstanding balances
python invoice_report.py aging
```

### Service Providers

Track project-based work with multiple line items and milestones.

```bash
python invoice_forge.py create startup_co \
  --item "Website Design - Phase 1" 1 3500.00 \
  --item "Logo Design" 1 800.00 \
  --item "Brand Guidelines Document" 1 500.00 \
  --discount-percent 5 \
  --notes "Milestone 1 of 3 - Design Phase"
```

---

## Configuration Reference

### Business Profile

```python
BUSINESS_NAME = "Your Business Name"
BUSINESS_ADDRESS = """123 Main Street
Suite 456
City, State 12345"""
BUSINESS_EMAIL = "billing@yourbusiness.com"
BUSINESS_PHONE = "+1 (555) 123-4567"
BUSINESS_LOGO = None  # Path to logo image (optional)
PAYMENT_DETAILS = """Bank Transfer: ...
PayPal: billing@yourbusiness.com"""
```

### Invoice Settings

```python
INVOICE_PREFIX = "INV-"  # Invoice number prefix
INVOICE_START = 1        # Starting number
INVOICE_PADDING = 4      # Zero-pad to 4 digits (INV-0001)
DEFAULT_PAYMENT_TERMS = 30  # Net 30
```

### Currency

```python
CURRENCY_SYMBOL = "$"
CURRENCY_CODE = "USD"
```

### Taxes

```python
TAX_RATES = {
    "sales_tax": 0.08,  # 8%
    "vat": 0.20,        # 20%
}
DEFAULT_TAX_TYPE = "sales_tax"
TAX_LABELS = {
    "sales_tax": "Sales Tax",
    "vat": "VAT",
}
```

### Recurring Templates

```python
RECURRING_TEMPLATES = {
    "monthly_retainer": {
        "description": "Monthly Retainer",
        "items": [{"description": "...", "quantity": 1, "rate": 5000.00}],
        "payment_terms": 15,
        "notes": "...",
    },
}
```

---

## File Structure

```
invoice-forge/
├── config_example.json         # Configuration template
├── config.json                 # Your config (create from example)
├── invoice_forge.py          # Main invoice engine
├── invoice_clients.py        # Client management
├── invoice_report.py         # Reports and analytics
├── invoice_template.py       # HTML/Markdown/Text rendering
├── data/
│   ├── clients.jsonl         # Client database
│   └── invoices.jsonl        # Invoice ledger
└── output/
    ├── INV-0001.html         # Generated invoices
    ├── INV-0002.html
    └── ...
```

All data is stored as **JSONL** (JSON Lines) for:
- **Human readability** - easy to grep, diff, and version control
- **Append-only safety** - no risk of corruption
- **Easy backup** - just copy the files

---

## Data Format

### Clients (data/clients.jsonl)

```json
{"client_id": "client001", "name": "John Doe", "email": "john@example.com", "address": "...", "phone": "...", "created_at": "...", "updated_at": "..."}
```

### Invoices (data/invoices.jsonl)

```json
{"invoice_number": "INV-0001", "invoice_date": "2024-01-15", "due_date": "2024-02-14", "client": {...}, "items": [...], "subtotal": 3000.00, "tax_amount": 240.00, "total": 3240.00, "status": "pending", ...}
```

---

## Tips & Best Practices

### Version Control Your Invoices

Keep your invoices under version control (git) for:
- Full audit trail
- Easy rollback if something breaks
- Backup and recovery

```bash
git init
git add data/ output/
git commit -m "January invoices"
```

### Backup Regularly

The `data/` folder contains your entire business ledger. Back it up!

```bash
# Simple backup
cp -r data/ data-backup-$(date +%Y%m%d)

# Or use git
git add data/
git commit -m "Backup $(date)"
```

### Use Recurring Templates

If you bill the same thing regularly (monthly retainers, subscriptions), set up templates in `config.json`. Saves time and ensures consistency.

### Check for Overdue Invoices Weekly

```bash
python invoice_report.py overdue
```

Set a reminder to run this every Monday morning. Follow up promptly.

### Generate Tax Reports

Revenue by month helps with quarterly/annual tax filing:

```bash
python invoice_report.py revenue --period month
```

### Print-to-PDF for Clients

The HTML invoices are print-ready. Open in browser, print to PDF, send to clients.

---

## Python API

You can also use Invoice Forge as a library:

```python
from invoice_forge import InvoiceForge

# Initialize
forge = InvoiceForge()

# Create invoice
invoice = forge.create_invoice(
    client_id="client001",
    items=[
        {"description": "Web Design", "quantity": 1, "rate": 2500.00},
        {"description": "Hosting Setup", "quantity": 1, "rate": 500.00},
    ],
    discount={"type": "percent", "value": 10},
    notes="Thank you for your business!",
)

# Render as HTML
html = forge.render_invoice(invoice, format="html")

# Save to file
filepath = forge.save_rendered_invoice(invoice, format="html")
print(f"Invoice saved to: {filepath}")
```

Client management:

```python
from invoice_clients import ClientManager

# Initialize
clients = ClientManager()

# Add client
client = clients.add_client(
    client_id="client001",
    name="John Doe",
    email="john@example.com",
    address="123 Main St",
    phone="+1-555-0100",
)

# Get client
client = clients.get_client("client001")

# List all clients
all_clients = clients.list_clients()

# Search clients
results = clients.list_clients(search="john")
```

Reports:

```python
from invoice_report import InvoiceReporter

# Initialize
reporter = InvoiceReporter()

# Overall summary
summary = reporter.get_overall_summary()
print(f"Total invoiced: ${summary['total_invoiced']:,.2f}")

# Overdue invoices
overdue = reporter.get_overdue_invoices()
print(f"{len(overdue)} invoice(s) overdue")

# Revenue by month
revenue = reporter.get_revenue_by_period("month")
for month, amount in revenue.items():
    print(f"{month}: ${amount:,.2f}")
```

---

## Requirements

- **Python 3.7+** (uses standard library only)
- **No external dependencies** - works out of the box

---

## Installation

```bash
# Clone or download
git clone <your-repo-url> invoice-forge
cd invoice-forge

# Set up config
cp config_example.json config.json
# Edit config.json with your business details

# Start invoicing!
python invoice_clients.py add client001 "John Doe" "john@example.com"
python invoice_forge.py create client001 --item "Service" 1 1000.00
```

---

## FAQ

**Q: Where is my data stored?**  
A: All data is in the `data/` folder as JSONL files. Human-readable, version-control friendly.

**Q: Can I customize the invoice template?**  
A: Yes! Edit `invoice_template.py` to change the HTML/CSS. The template is clean and well-commented.

**Q: How do I handle multiple tax rates?**  
A: Define them in `config.json` under `TAX_RATES`, then specify `--tax <type>` when creating invoices.

**Q: Can I add a logo?**  
A: Yes! Set `BUSINESS_LOGO = "logo.png"` in `config.json`. The logo will be embedded in HTML invoices.

**Q: How do I email invoices?**  
A: Invoice Forge generates the invoice files; emailing is separate. Use your email client or a script to send the HTML files as attachments.

**Q: Can I export to PDF directly?**  
A: The HTML template is print-ready. Open in browser, print to PDF. For automation, use a tool like `wkhtmltopdf` or headless Chrome.

**Q: What about recurring subscriptions?**  
A: Set up templates in `config.json`, then use `python invoice_forge.py template <name> <client>` to generate them quickly.

**Q: How do I migrate to a different system later?**  
A: Data is stored as JSONL (one JSON object per line). Easy to parse and import into any other system.

---

## Support

This is open-source software provided as-is under the MIT License. No support is guaranteed, but feel free to:

- Read the code (it's clean and well-commented)
- File issues or contribute improvements
- Fork and customize for your needs

---

## License

MIT License - see LICENSE file for details.

**Created by Shadow Rose**  
quality-verified for production use.

---

## Changelog

**v1.0.0** - Initial release
- Invoice generation (HTML, Markdown, plain text)
- Client management
- Payment tracking
- Reports and analytics
- Recurring templates
- Zero dependencies


---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** This software processes and stores data locally on your system. 
The author(s) are not responsible for data loss, corruption, or unauthorized access 
resulting from software bugs, system failures, or user error. Always maintain 
independent backups of important data. This software does not transmit data externally 
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)