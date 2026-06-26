# Payment Terms Guide

> Reference for understanding and applying payment terms.
> Load with `read_file("references/payment-terms-guide.md")` when setting up invoices or advising on terms.

---

## Standard Payment Terms

### Net Terms

| Term | Meaning | Best For |
|------|---------|----------|
| Due on receipt | Payment expected immediately | Small amounts, trusted clients |
| Net 7 | Due 7 days from invoice date | Rush work, small projects |
| Net 15 | Due 15 days from invoice date | Ongoing work with good clients |
| Net 30 | Due 30 days from invoice date | **Most common** — industry standard |
| Net 45 | Due 45 days from invoice date | Enterprise clients (common request) |
| Net 60 | Due 60 days from invoice date | Large enterprises, government |
| Net 90 | Due 90 days from invoice date | **Avoid if possible** — significant cash flow risk |

### Early Payment Discounts

| Term | Meaning | Example |
|------|---------|---------|
| 2/10 Net 30 | 2% discount if paid within 10 days, otherwise full amount due in 30 | $10,000 invoice → $9,800 if paid in 10 days |
| 1/15 Net 45 | 1% discount if paid within 15 days | Enterprise incentive |

**When to offer discounts:**
- Client consistently pays late on standard terms
- You need to accelerate cash flow
- Large invoice where 1-2% is worth the time value

**When NOT to offer:**
- Already tight margins
- Client always pays on time (you're giving away money)
- Small amounts where the discount is negligible

---

## Payment Structures

### Deposits / Advance Payments

| Structure | When to Use |
|-----------|-------------|
| 50% upfront, 50% on completion | Standard for project work |
| 100% upfront | Small projects, new/unknown clients |
| 30/30/40 split | Larger projects with 3 milestones |
| Monthly in advance | Retainer/subscription billing |

**Why deposits matter for solo entrepreneurs:**
- You can't absorb non-payment the way a large company can
- Deposits prove client commitment and ability to pay
- They fund your work during the project
- If the project is cancelled, you're not left with nothing

### Milestone-Based Billing

Break large projects into payment milestones tied to deliverables:

```
Milestone 1: Project kickoff + requirements     — 25% ($5,000)
Milestone 2: Design approval                     — 25% ($5,000)
Milestone 3: Development complete                 — 25% ($5,000)
Milestone 4: Launch + 30-day support              — 25% ($5,000)
```

**Rules:**
- Each milestone should have a clear, verifiable deliverable
- Define acceptance criteria upfront
- Invoice immediately upon milestone completion
- Don't start next milestone until previous is paid (if possible)

### Retainer / Subscription Billing

- Invoice at the start of each service period (in advance)
- State the service period clearly: "Services for April 2026"
- Include rollover/expiry rules if applicable
- Auto-generate using recurring invoice templates

### Hourly / Time-Based Billing

- Invoice at the end of each billing period (in arrears)
- Include timesheet summary or attach detailed log
- State the rate, hours, and period clearly
- Consider a cap or estimate to manage client expectations

---

## Terms Selection for Solo Entrepreneurs

### Recommended Defaults

| Client Type | Recommended Terms | Why |
|-------------|-------------------|-----|
| New client, no history | 50% deposit + Net 15 balance | Reduce risk |
| Established client, good payer | Net 30 | Industry standard |
| Enterprise / large company | Net 30 (push back on Net 60+) | Protect cash flow |
| Government / institutional | Net 30-45 (per their policy) | Often non-negotiable |
| One-off small project | Due on receipt or Net 7 | Not worth chasing |
| Recurring retainer | Due on receipt, monthly in advance | Simplest cash flow |

### Negotiation Guidance

**Client asks for Net 60:**
- Counter with Net 30
- If they insist: Net 45 with early payment discount (2/10)
- If non-negotiable: build the financing cost into your rate
- Red flag if combined with large scope and no deposit

**Client asks for Net 90:**
- Almost always unfavorable for a solo entrepreneur
- Counter: Net 30 with milestone payments
- If forced to accept: require a larger deposit
- Factor the 90-day float into pricing

**Client wants to pay on completion only:**
- Counter: deposit + milestone structure
- Define "completion" precisely (avoid scope creep blocking payment)
- Include acceptance period with auto-acceptance clause

---

## Due Date Calculation

### Rules

1. **Always calculate and state the explicit due date** — don't rely on the client computing it
2. **Start from issue date**, not delivery date or receipt date
3. **Business days vs. calendar days** — most terms use calendar days unless specified
4. **End-of-month considerations** — if due date falls on a weekend/holiday, the next business day applies

### Examples

| Invoice Date | Terms | Due Date |
|-------------|-------|----------|
| March 1, 2026 | Net 30 | March 31, 2026 |
| March 15, 2026 | Net 30 | April 14, 2026 |
| March 1, 2026 | Net 15 | March 16, 2026 |
| March 1, 2026 | Due on receipt | March 1, 2026 |

---

## Late Fees

### When to Include

- Only if your contract/agreement allows it
- State the clause on the invoice: "Per agreement, a late fee of 1.5% per month applies to overdue balances."
- Check jurisdictional limits on interest rates (escalate if unsure)

### Common Structures

| Type | Example | Notes |
|------|---------|-------|
| Monthly percentage | 1.5% per month | Most common for B2B |
| Annual percentage | 18% per annum | Same as 1.5%/month |
| Flat fee | $25 per late payment | Simple, predictable |
| Daily rate | 0.05% per day | Precise but aggressive |

### Practical Advice

- Having a late fee clause is more valuable as a deterrent than a revenue source
- Enforcing late fees can strain relationships — use judgment
- For chronic late payers: enforce consistently, or renegotiate terms
- For one-time late payment from a good client: consider waiving

---

## Payment Methods

### Common Methods for Solo Entrepreneurs

| Method | Pros | Cons |
|--------|------|------|
| Bank transfer / ACH | Low fees, reliable | Slow (1-3 days), requires sharing bank details |
| Wire transfer | Fast for international | Higher fees ($15-50) |
| PayPal / Stripe | Easy, instant confirmation | 2.9% + fees |
| Check | Client preference | Slow, can bounce |
| Credit card | Convenient for client | Processing fees |
| Cryptocurrency | Fast international | Volatile, tax complexity |

### Payment Instructions on Invoices

Always include:
- **Preferred method** with full details (account number, routing, IBAN, PayPal email)
- **Reference to include** — invoice number, so you can match payments
- **Alternative method** if available

Example:
```
Bank Transfer (preferred):
  Bank: First National Bank
  Account Name: Your Business LLC
  Account: XXXX-XXXX-1234
  Routing: 021000021
  Reference: INV-2026-003

Or pay via PayPal: payments@yourbusiness.com
Please include invoice number in payment reference.
```

---

## Multi-Currency Considerations

- State the invoice currency explicitly
- If client pays in a different currency, note whose exchange rate applies
- Consider currency risk for Net 60+ terms on foreign currency invoices
- Track receivables in the invoice currency, not your home currency
- **Exchange rate disputes** — define in the contract which rate/source/date applies

---

*Reference for opc-invoice-manager. Not financial advice.*
