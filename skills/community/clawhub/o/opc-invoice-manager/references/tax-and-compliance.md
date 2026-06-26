# Tax & Compliance Awareness

> General tax awareness for invoicing — NOT tax advice.
> Load with `read_file("references/tax-and-compliance.md")` when tax questions arise.

**This is an invoicing tool, not tax advice. Consult a qualified accountant for tax compliance decisions.**

---

## Escalate-to-Accountant Triggers

When any of these topics arise, output:

```
🧾 **ACCOUNTANT RECOMMENDED**: [specific reason].
This is an invoicing tool, not tax advice. Consult a qualified accountant.
```

### Mandatory Escalation List

1. **Cross-border invoicing** — VAT, withholding tax, treaty implications
2. **VAT/GST registration thresholds** — approaching or exceeding registration limits
3. **Revenue thresholds** — income levels that may trigger tax status changes
4. **Withholding tax** — client requests to withhold tax from payment
5. **Multiple-entity billing** — invoicing through different legal entities
6. **Year-end tax reporting** — filing, estimated payments, annual returns
7. **Transfer pricing** — intercompany or related-party invoicing
8. **Credit notes with tax implications** — refunds that affect collected tax
9. **Disputed amounts with accounting impact** — disputes that may require accrual adjustments
10. **Tax-exempt status questions** — whether an exemption applies
11. **Digital services tax** — jurisdiction-specific rules for digital/SaaS services
12. **Permanent establishment risk** — invoicing patterns that suggest PE in another jurisdiction
13. **Reverse charge mechanism** — when the buyer self-assesses tax
14. **Tax ID format validation** — verifying a tax ID is valid for a jurisdiction

---

## General Tax Awareness (What the Skill CAN Do)

The skill can help with these invoice-level actions without providing tax advice:

### Tax Line Items on Invoices

- **Add tax lines** when the user specifies the rate and type
- **Calculate tax amounts** from a given rate (e.g., "20% VAT on subtotal")
- **Display multiple tax lines** (federal + state, VAT + local)
- **Mark items as tax-exempt** with a reason field
- **Show tax-inclusive vs. tax-exclusive** totals when specified

### Tax Fields in Metadata

```json
{
  "tax_details": [
    {
      "tax_name": "VAT",
      "tax_rate": "20%",
      "tax_amount": "2000.00",
      "tax_exempt": false
    }
  ],
  "total_tax": "2000.00"
}
```

### What the Skill Should NOT Do

- **Determine which tax applies** — user or accountant decides
- **Assert compliance** with any jurisdiction's tax law
- **Calculate tax for unfamiliar jurisdictions** without user-provided rates
- **Advise on tax registration** requirements
- **Determine if reverse charge applies** — only apply if user confirms
- **File or report** tax to any authority

---

## Common Tax Scenarios for Solo Entrepreneurs

### Domestic B2B Invoicing

- Usually straightforward — apply local tax rate if registered
- If tax-exempt (e.g., B2B in some jurisdictions), note the exemption reason
- Include your tax ID and client's tax ID on the invoice

### Domestic B2C Invoicing

- Tax typically required at point of sale
- Rate depends on jurisdiction and product/service type
- Some services may be exempt — **escalate if unsure**

### International Invoicing

**Always escalate to accountant.** Common considerations:

| Scenario | Typical Treatment | Action |
|----------|-------------------|--------|
| B2B export of services | Often zero-rated or reverse-charged | Escalate — rules vary by jurisdiction |
| B2C cross-border digital | May require registration in buyer's jurisdiction | Escalate |
| Withholding tax | Client withholds % from payment | Escalate — affects net receivable |
| Treaty benefits | Reduced withholding rates | Escalate — requires documentation |

### Tax-Exempt Invoicing

Valid reasons to mark an invoice as tax-exempt:
- Client provided tax exemption certificate
- B2B reverse charge applies (confirm with accountant)
- Service type is exempt in the jurisdiction
- Export of services (zero-rated)

**Always document the reason** in both the invoice and metadata.

---

## Compliance Basics (Not Jurisdiction-Specific)

### Invoice Retention

- Most jurisdictions require keeping invoices for 5–10 years
- Keep both issued invoices and received invoices
- Digital storage is generally acceptable
- The skill's archive structure supports long-term retention

### Sequential Numbering

- Many jurisdictions require sequential invoice numbering
- Gaps must be explainable (voided invoices)
- The skill's numbering system enforces this

### Required Invoice Fields by Region (General Guidance)

Most jurisdictions require some combination of:
- Seller and buyer identification (name, address, tax ID)
- Invoice number and date
- Description of goods/services
- Amounts with tax breakdown
- Payment terms

**Specific requirements vary by jurisdiction** — escalate for compliance verification.

### E-Invoicing Requirements

Some jurisdictions require electronic invoicing in specific formats:
- EU: EN 16931 standard, Peppol network
- India: GST e-invoicing through IRP
- Brazil: NF-e
- Italy: FatturaPA through SDI

**If a client requires a specific e-invoicing format, escalate.** This skill generates standard invoices, not jurisdiction-specific e-invoice formats.

---

## Tax Rate Handling in the Skill

### User-Provided Rates

The skill applies tax rates the user provides. It does NOT determine rates.

```
User: "Add 20% VAT"
Skill: Adds tax line with 20% rate, calculates amount, displays on invoice.

User: "What tax rate should I use?"
Skill: "🧾 ACCOUNTANT RECOMMENDED: Tax rate determination depends on your
jurisdiction, registration status, and the nature of the service.
This is an invoicing tool, not tax advice."
```

### Multiple Tax Rates

Support for:
- Different rates per line item (some items exempt, some taxed)
- Multiple tax types on the same invoice (VAT + local tax)
- Compound vs. simple tax calculation (user specifies which)

### Tax on Discounts

- Apply tax after discount (most common)
- User can specify if discount is pre-tax or post-tax
- **If unsure about tax treatment of discounts, escalate**

---

## Late Fees & Interest

### What the Skill Can Do

- Calculate late fee amounts based on user-provided rates
- Add late fee line items to follow-up invoices
- Reference the contractual late fee clause

### What Requires Caution

- Maximum allowable interest rates vary by jurisdiction
- Some jurisdictions regulate late fee practices
- If the client is in a different jurisdiction, rules may differ
- **Escalate if unsure about late fee legality**

---

## Key Principle

**When in doubt, escalate.** The cost of wrong tax treatment is far higher than the cost of asking an accountant. The skill's job is to create clean, complete invoices — tax compliance is the accountant's domain.

---

*Reference for opc-invoice-manager. This is NOT tax advice. Consult a qualified accountant.*
