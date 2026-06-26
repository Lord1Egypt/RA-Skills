# Invoice Best Practices

> Reference for creating professional, clear, and payment-optimized invoices.
> Load with `read_file("references/invoice-best-practices.md")` when generating or reviewing invoices.

---

## Invoice Content Essentials

### Required Elements

Every invoice MUST include:

1. **Invoice number** — unique, sequential, no gaps (gaps require explanation)
2. **Issue date** — date the invoice is created and sent
3. **Due date** — explicit date, not just "Net 30" (calculate and state the date)
4. **Your entity details** — legal name, address, tax ID, contact email
5. **Client details** — legal billing name, billing address, attention line
6. **Line items** — description, quantity, unit price, line total
7. **Subtotal, tax, discount, total** — clearly broken out
8. **Currency** — stated explicitly, especially for international clients
9. **Payment instructions** — how to pay (bank details, payment link, etc.)

### Recommended Elements

- **Reference / PO number** — critical if client requires PO for payment processing
- **Service period** — "Services for March 2026" or "Jan 15 – Feb 14, 2026"
- **Contract reference** — links invoice to governing agreement
- **Payment terms** — "Net 30", "Due on receipt", etc.
- **Late fee notice** — if contractually agreed, state it on the invoice
- **Notes** — scope clarifications, thank-you message, next billing date

---

## Numbering Best Practices

### Format Principles

- **Sequential and unique** — never reuse a number, even for voided invoices
- **Predictable** — client should be able to tell the order from the number
- **Informative** — encode year/month for easy filing (e.g., `INV-2026-001`)
- **Consistent** — once you pick a format, stick with it

### Common Formats

| Format | Example | Best For |
|--------|---------|----------|
| `INV-{YYYY}-{NNN}` | INV-2026-001 | Most solo businesses |
| `INV-{YYYY}{MM}-{NNN}` | INV-202603-001 | High-volume monthly billing |
| `{CLIENT}-{YYYY}-{NNN}` | ACME-2026-001 | Client-segregated numbering |
| `{NNN}` | 001 | Simplest, works for low volume |

### Reset Policies

- **Yearly reset** (recommended) — restart sequence each January. `INV-2026-001`, `INV-2027-001`
- **Never reset** — single continuous sequence. Simplest but numbers grow large.
- **Monthly reset** — restart each month. Only if format includes month.

### Voided Numbers

- **Never reuse** voided invoice numbers
- Mark as void in the index with a reason
- The gap is the audit trail

---

## Formatting & Presentation

### Line Item Descriptions

**Bad**: "Services" / "Work" / "Consulting"
**Good**: "Frontend development — user authentication module (40 hrs @ $150/hr)"

Rules:
- Be specific enough that the client knows what they're paying for
- Include dates or sprint references if applicable
- Match the language of the contract/SOW where possible
- Group related work into logical line items (not one mega-line, not 50 micro-lines)

### Line Item Types

| Type | When to Use |
|------|-------------|
| `hourly` | Time-based billing with rate × hours |
| `fixed` | Fixed-price deliverable or flat fee |
| `milestone` | Contract milestone completion |
| `recurring` | Monthly/quarterly retainer or subscription |
| `expense` | Reimbursable expense (attach receipts) |

### Currency & Amounts

- Always state the currency code (USD, EUR, GBP) — never assume
- Use consistent decimal places (2 for most currencies)
- Use the client's expected currency unless contract specifies otherwise
- For multi-currency situations, state the exchange rate and source date
- Store amounts as strings in JSON to avoid floating-point rounding

### Tax Display

- Show tax as a separate line: "VAT (20%)" or "Sales Tax (8.875%)"
- If tax-exempt, state why: "Tax exempt — B2B reverse charge" or "Tax exempt per certificate on file"
- Multiple tax lines are fine (federal + state, VAT + withholding)
- **Never calculate tax you're unsure about** — flag for accountant review

---

## Timing & Delivery

### When to Invoice

| Billing Model | When to Invoice |
|---------------|-----------------|
| Monthly retainer | 1st of the service month (invoice in advance) |
| Hourly/time-based | End of billing period (invoice in arrears) |
| Milestone | Upon milestone completion and acceptance |
| Project fixed-fee | Per contract schedule (often: deposit → milestones → final) |
| Expense reimbursement | With the next regular invoice, or monthly |

### Delivery Best Practices

1. **Send early in the week** — Tuesday/Wednesday invoices get processed faster than Friday invoices
2. **Send in the morning** — more likely to be seen same-day
3. **Use the right channel** — if client has a vendor portal, use it; otherwise email to AP
4. **CC the right people** — your business contact AND their AP contact
5. **Include the invoice as attachment** — PDF or HTML, not just inline text
6. **Write a clear subject line** — "Invoice INV-2026-003 — $5,000 — Due April 15"
7. **Keep the email body short** — the invoice has the details

### Service Period Labels

For recurring invoices, make the period crystal clear:
- "Services for March 2026"
- "Q1 2026 retainer (January – March)"
- "Weekly support — March 3–9, 2026"

---

## Common Mistakes

| Mistake | Why It Matters | Fix |
|---------|---------------|-----|
| No PO number | Client's AP can't process without it | Ask for PO before invoicing |
| Wrong billing entity name | Payment goes to wrong entity or gets rejected | Match the contract exactly |
| Vague descriptions | Client disputes or delays payment | Be specific per contract scope |
| Missing due date | No urgency, gets deprioritized | Always calculate and state the date |
| Sending to wrong contact | Business contact ≠ AP contact | Maintain AP contact in client profile |
| Rounding errors | Amounts don't add up, looks unprofessional | Verify arithmetic: subtotal + tax - discount = total |
| No payment instructions | Client doesn't know how to pay | Include bank details or payment link |
| Late invoicing | Harder to collect the longer you wait | Invoice promptly per billing cycle |

---

## Invoice as a Professional Document

The invoice represents your business. It should be:

- **Clean and readable** — consistent formatting, adequate whitespace
- **Complete** — all required information present
- **Accurate** — amounts, dates, and details match the contract
- **Professional** — no typos, no tool disclaimers, no draft watermarks on final versions
- **Branded** — your company name/logo, consistent with other business documents

The invoice is a customer-facing document. Internal notes, AI tool attributions, and processing metadata belong in the metadata file, not on the invoice itself.

---

*Reference for opc-invoice-manager. Not legal or tax advice.*
