# Invoice Generator

Create professional invoices in Markdown format. Supports multiple currencies, tax calculations, and standard invoice fields. Perfect for freelancers, consultants, and small businesses.

## When to use

Use this skill when the user needs to:
- Create a professional invoice for a client
- Generate recurring invoices
- Calculate totals with tax, discounts, and multiple line items
- Format an invoice in a printable Markdown layout
- Convert invoice details into a structured document

## How it works

1. Ask for sender details (business name, address, email, payment info)
2. Ask for recipient details (client name, company, address)
3. Ask for line items (description, quantity, unit price)
4. Ask for currency, tax rate, discount, and payment terms
5. Generate a complete professional invoice in Markdown

## Invoice Template

```markdown
# INVOICE

**Invoice #:** [AUTO-INCREMENT or USER-PROVIDED]
**Date:** [CURRENT DATE]
**Due Date:** [DATE + PAYMENT TERMS]

---

**From:**
[Business Name]
[Address Line 1]
[Address Line 2]
[Email] | [Phone]

**Bill To:**
[Client Name]
[Client Company]
[Client Address]
[Client Email]

---

## Items

| # | Description | Qty | Unit Price | Amount |
|---|-------------|-----|-----------|--------|
| 1 | [Service/Product] | [Qty] | [Price] | [Total] |
| 2 | [Service/Product] | [Qty] | [Price] | [Total] |

---

|  | |
|---|---|
| **Subtotal** | [CURRENCY] [AMOUNT] |
| **Tax ([RATE]%)** | [CURRENCY] [AMOUNT] |
| **Discount** | -[CURRENCY] [AMOUNT] |
| **TOTAL DUE** | **[CURRENCY] [AMOUNT]** |

---

## Payment Details

**Payment Method:** [Bank Transfer / PayPal / Stripe / etc.]
**Bank:** [Bank Name]
**Account:** [Account Number]
**Routing:** [Routing Number]

**Payment Terms:** [Net 30 / Due on Receipt / etc.]

---

*Thank you for your business!*
```

## Supported Currencies

USD ($), EUR (€), GBP (£), JPY (¥), CAD (C$), AUD (A$), CHF, INR (₹), BRL (R$), KRW (₩), and more. Format amounts according to locale conventions.

## Calculation Rules

- Subtotal = Sum of (quantity × unit price) for all line items
- Tax = Subtotal × tax rate
- Discount can be percentage or fixed amount
- Total = Subtotal + Tax - Discount
- Round to 2 decimal places (0 for JPY/KRW)

## Output

Generate a clean Markdown invoice that:
- Is print-ready when rendered
- Uses proper currency formatting
- Includes all required fields
- Has clear visual hierarchy with horizontal rules
- Can be easily copied and converted to PDF
