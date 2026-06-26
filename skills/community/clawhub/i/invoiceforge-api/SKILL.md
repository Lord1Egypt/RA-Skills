---
name: invoiceforge-api
description: "Generate professional PDF invoices using InvoiceForge API - create, manage, and download invoices for freelancers, agencies, consultants, small businesses, SaaS companies, contractors, invoice generation, billing automation, PDF invoices, accounts receivable, client billing, professional invoices, automated invoicing, invoice templates, payment tracking, invoice management, financial documents, receipt generation, billing system, and any invoicing or billing needs."
---

# InvoiceForge API Skill

Generate professional PDF invoices using VCG's InvoiceForge API — pure software invoice generation with automatic calculations, PDF rendering, and invoice management.

## Quick Start

1. **Get API Key**: Help user sign up for free InvoiceForge API key
2. **Store Key**: Save the key securely
3. **Create Invoices**: Generate professional PDF invoices from structured data

## API Key Signup

### Step 1: Get User's Email
Ask the user for their email address to create a free InvoiceForge account.

### Step 2: Sign Up via API
```bash
curl -X POST https://invoiceforge.vosscg.com/v1/keys \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'
```

**Expected Response:**
```json
{
  "api_key": "your-api-key-here",
  "plan": "free"
}
```

### Step 3: Store the API Key
Save the API key securely for future use.

## Creating Invoices

### Create a Full Invoice
```bash
curl -X POST https://invoiceforge.vosscg.com/v1/invoices \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "seller": {
      "name": "Acme Consulting",
      "email": "billing@acme.com",
      "address": "123 Main St, San Francisco, CA 94102"
    },
    "buyer": {
      "name": "Widget Corp",
      "email": "ap@widget.com",
      "address": "456 Oak Ave, New York, NY 10001"
    },
    "items": [
      {"description": "Strategy Consulting - March 2026", "quantity": 40, "unit_price": 250.00},
      {"description": "Travel Expenses", "quantity": 1, "unit_price": 1200.00}
    ],
    "tax_rate": 8.5,
    "currency": "USD",
    "due_date": "2026-04-15",
    "notes": "Net 30. Wire transfer preferred."
  }'
```

**Expected Response:**
```json
{
  "invoice_number": "INV-000001",
  "subtotal": 11200.00,
  "tax_rate": 8.5,
  "tax_amount": 952.00,
  "total": 12152.00,
  "currency": "USD",
  "status": "draft",
  "created_at": "2026-03-04T...",
  "download_url": "/v1/invoices/INV-000001/pdf"
}
```

### Download Invoice PDF
```bash
curl -H "X-API-Key: YOUR_KEY" \
  https://invoiceforge.vosscg.com/v1/invoices/INV-000001/pdf \
  -o invoice.pdf
```

### List All Invoices
```bash
curl -H "X-API-Key: YOUR_KEY" \
  "https://invoiceforge.vosscg.com/v1/invoices?status=draft&page=1&limit=20"
```

### Update Invoice Status
```bash
curl -X PATCH https://invoiceforge.vosscg.com/v1/invoices/INV-000001/status \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "sent"}'
```

Valid statuses: `draft`, `sent`, `paid`, `void`

## Common Use Cases

### Freelancer Monthly Invoice
When a user says "create an invoice for my client":
1. Ask for seller info (their business name, email, address)
2. Ask for buyer info (client name, email, address)
3. Ask for line items (services, hours, rates)
4. Ask for tax rate and due date
5. Create the invoice via API
6. Download and share the PDF

### Batch Invoicing
Create multiple invoices by looping through client data. Each POST creates a new invoice with auto-incrementing numbers.

### Invoice Tracking
Use the list endpoint with status filters to track:
- `draft` — Created but not sent
- `sent` — Delivered to client
- `paid` — Payment received
- `void` — Cancelled

## Supported Currencies
Any 3-letter ISO 4217 code: USD, EUR, GBP, CAD, AUD, JPY, etc.

## Rate Limits
- **Free tier**: 100 requests/day, 50 invoices/month
- **Pro tier**: Unlimited (Stripe billing)

## API Base URL
```
https://invoiceforge.vosscg.com
```

## Endpoints Summary
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/keys | Create API key |
| POST | /v1/invoices | Create invoice |
| GET | /v1/invoices | List invoices |
| GET | /v1/invoices/:id/pdf | Download PDF |
| PATCH | /v1/invoices/:id/status | Update status |
| GET | /v1/health | Health check |
| GET | /v1/metrics | Service metrics |

## Error Handling
- `400` — Validation error (missing fields, bad data)
- `401` — Missing or invalid API key
- `404` — Invoice not found
- `403` — Access denied (not your invoice)
- `429` — Rate limit exceeded
