# Limitations

Invoice Forge is designed for simplicity and self-contained operation. This comes with some trade-offs.

---

## What Invoice Forge Does NOT Do

### 1. Email Integration

Invoice Forge **generates** invoices but does **not send them**.

You'll need to:
- Open the generated HTML file in a browser
- Print to PDF or attach the HTML directly
- Send via your email client or scripting

**Why:** Email requires SMTP configuration, credentials, and error handling. Keeping this separate means:
- No credentials in the config file
- Use your existing email workflow
- One less thing to break

**Workaround:** Use a simple email script or your email client's "attach file" feature.

---

### 2. Direct PDF Export

Invoice Forge generates **HTML** (print-ready) but not PDF directly.

To get PDF:
- Open HTML invoice in browser → Print → Save as PDF
- Use a command-line tool like `wkhtmltopdf` or headless Chrome
- Integrate with a PDF library (e.g., ReportLab, WeasyPrint) if you need automation

**Why:** PDF generation requires external dependencies or heavyweight libraries. The HTML output is print-ready and works everywhere.

**Workaround:** The HTML template is designed for perfect print-to-PDF rendering.

---

### 3. Payment Gateway Integration

Invoice Forge does **not** integrate with Stripe, PayPal, or other payment processors.

It tracks payment **status** (pending, paid, overdue) but doesn't:
- Generate payment links
- Process credit cards
- Automatically update status when paid

**Why:** Payment integration is complex, provider-specific, and requires credentials. Most freelancers and small businesses use separate payment systems.

**Workaround:** 
- Add payment links manually in `config.json` under `PAYMENT_DETAILS`
- Update invoice status manually when payment received
- Use webhooks from your payment provider to trigger status updates (requires custom scripting)

---

### 4. Multi-User / Team Collaboration

Invoice Forge is **single-user** by design.

There's no:
- User authentication
- Role-based permissions
- Concurrent access control
- Conflict resolution

**Why:** Multi-user support requires database locking, authentication, and UI. This is built for solo freelancers and small businesses.

**Workaround:** 
- Use shared folders (Dropbox, git) for data syncing between devices
- Treat the JSONL files as the source of truth
- Use git for version control and audit trail

---

### 5. Cloud Sync / SaaS

Invoice Forge is **local-first** and **self-hosted**.

There's no:
- Cloud storage
- Web dashboard
- Mobile app
- Remote access

**Why:** Cloud means hosting, security, maintenance, and ongoing costs. Local-first means:
- Your data stays on your machine
- No subscription fees
- Works offline
- No vendor lock-in

**Workaround:** 
- Use Dropbox/Google Drive to sync the `data/` folder across devices
- Access via SSH if you need remote access
- Run on a server if you want team access (bring your own auth)

---

### 6. Advanced Reporting / Charts

Reports are **text-based summaries**, not interactive dashboards.

There's no:
- Graphs or charts
- Trend analysis
- Forecasting
- Visual analytics

**Why:** Charting requires external libraries (matplotlib, plotly) or web frameworks. Keeping it simple means easy auditing and scripting.

**Workaround:**
- Export data to CSV and use Excel/Google Sheets for charts
- Pipe report output to other tools (gnuplot, R, Python notebooks)
- The JSONL format is easy to parse for custom analysis

---

### 7. Time Tracking Integration

Invoice Forge does **not track time** or integrate with time-tracking tools.

You need to:
- Track hours separately (Toggl, Harvest, spreadsheet, etc.)
- Manually create line items based on tracked time

**Why:** Time tracking is a separate concern. Most freelancers already have a preferred tool.

**Workaround:**
- Use your time tracker's export feature
- Create invoice items from exported data
- Script the conversion if you do it regularly

---

### 8. Inventory / Product Catalog

Invoice Forge has **no product database**.

Each invoice requires manually specifying:
- Description
- Quantity
- Rate

There's no:
- Product SKUs
- Inventory tracking
- Stock management

**Why:** This is for services and simple products, not retail inventory.

**Workaround:**
- Use recurring templates for standard offerings
- Keep a separate product list and copy-paste
- Script product imports if you have a large catalog

---

### 9. Multi-Currency Support

Invoice Forge supports **one currency per installation**.

You can set the currency symbol and code in `config.json`, but:
- All invoices use the same currency
- No automatic currency conversion
- No multi-currency reporting

**Why:** Currency conversion requires real-time rates, decimal precision handling, and accounting complexity.

**Workaround:**
- Run separate installations for different currencies
- Manually convert amounts before invoicing
- Note the exchange rate in invoice notes

---

### 10. Automatic Late Fees

Invoice Forge **flags** overdue invoices but does **not automatically add late fees**.

You need to:
- Check overdue reports manually
- Send reminders
- Add late fees as separate line items if needed

**Why:** Late fee policies vary widely (percentage, flat fee, grace periods). Automation risks legal/customer issues.

**Workaround:**
- Run `python invoice_report.py overdue` weekly
- Follow up manually
- Create a new invoice with late fees if appropriate

---

### 11. Tax Compliance / Filing

Invoice Forge **calculates** tax amounts but does **not file taxes** or ensure compliance.

You're responsible for:
- Setting correct tax rates
- Filing with tax authorities
- Following local regulations
- Keeping records

**Why:** Tax law varies by jurisdiction and changes frequently. This is accounting software, not legal advice.

**Workaround:**
- Consult with an accountant for tax rates and rules
- Use the revenue reports to prepare tax filings
- Keep the `data/invoices.jsonl` file as your audit trail

---

### 12. Bank Integration

Invoice Forge does **not connect to banks** or import transactions.

Payment tracking is **manual**:
- Check your bank account
- Update invoice status: `python invoice_forge.py status INV-0001 paid`

**Why:** Bank integration requires API credentials, OAuth, and security compliance.

**Workaround:**
- Use bank exports (CSV/OFX) and cross-reference manually
- Script status updates if you have a regular import process

---

## What Invoice Forge IS For

Invoice Forge is **perfect** for:

- **Freelancers** who need simple, professional invoicing without monthly fees
- **Solo consultants** tracking a handful of clients
- **Small businesses** with straightforward invoicing needs
- **Anyone who values**:
  - Local data ownership
  - No vendor lock-in
  - Simple, auditable files
  - Zero dependencies
  - Works-offline reliability

---

## What It's NOT For

Invoice Forge is **not ideal** for:

- Large agencies with dozens of team members
- Businesses needing real-time payment processing
- Retail operations with inventory management
- Organizations requiring SOC2/HIPAA compliance
- Teams needing collaborative workflows
- Anyone wanting a web dashboard or mobile app

For those use cases, consider:
- **FreshBooks** (cloud, full-featured)
- **QuickBooks** (accounting + invoicing)
- **Zoho Invoice** (team collaboration)
- **Wave** (free, cloud-based)

Invoice Forge is the **scrappy, local-first alternative** that prioritizes simplicity, ownership, and reliability over features.

---

## Known Issues

### 1. JSONL File Corruption

If you manually edit `data/clients.jsonl` or `data/invoices.jsonl` and introduce invalid JSON, the file may become unreadable.

**Mitigation:**
- Use the CLI tools instead of editing files directly
- Keep backups (git or file copies)
- Validate JSON before saving if editing manually

---

### 2. Invoice Number Conflicts

If you run multiple instances or manually set invoice numbers, you may get duplicates.

**Mitigation:**
- Use different `INVOICE_PREFIX` values for different installations
- Let the system auto-generate numbers
- Check for conflicts: `grep "INV-0001" data/invoices.jsonl`

---

### 3. No Transaction Safety

JSONL files are append-only, but if two processes write simultaneously, corruption is possible.

**Mitigation:**
- Don't run multiple invoice creation commands at once
- Use file locking if scripting bulk operations
- Regular backups

---

### 4. Large Files = Slow Searches

JSONL is scanned sequentially. With thousands of invoices, searches may slow down.

**Mitigation:**
- Archive old data periodically (move to separate files by year)
- Use `grep` for quick searches
- Script custom indexes if needed

---

## Philosophy

Invoice Forge is **intentionally simple**.

The limitations above are **design choices**, not bugs:
- No database = no migrations, no corruption
- No cloud = no downtime, no data breaches
- No auth = no password resets, no account recovery
- No framework = no bloat, no security patches

If you need more features, fork it! The code is MIT-licensed and easy to extend.

But if you just need to:
- Generate professional invoices
- Track who owes you money
- Get paid

Then Invoice Forge does the job. Reliably. Forever.

---

**Bottom line:** Invoice Forge is a tool, not a service. It does one thing well: generate and track invoices locally with zero dependencies. Everything else is up to you.
