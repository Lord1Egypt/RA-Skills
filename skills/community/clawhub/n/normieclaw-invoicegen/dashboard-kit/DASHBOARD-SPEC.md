# InvoiceGen Dashboard Kit Specification

Your InvoiceGen purchase includes a beautiful local dashboard to track outstanding balances and revenue visually.

## Database Schema (SQLite)

The dashboard relies on a lightweight, local SQLite database for speed and privacy.

### `Users`
- `id` (PK, TEXT)
- `business_name` (TEXT)
- `address` (TEXT)
- `email` (TEXT)
- `logo_path` (TEXT)
- `brand_color` (TEXT, e.g., "#0F172A")
- `payment_details` (TEXT)

### `Clients`
- `id` (PK, TEXT)
- `name` (TEXT)
- `email` (TEXT)
- `address` (TEXT)
- `default_terms` (TEXT)
- `tax_rate` (REAL)
- `currency` (TEXT)

### `Invoices`
- `id` (PK, TEXT)
- `invoice_number` (TEXT, e.g., "INV-1042")
- `client_id` (FK -> Clients.id)
- `issue_date` (TEXT, ISO8601)
- `due_date` (TEXT, ISO8601)
- `subtotal` (REAL)
- `tax_amount` (REAL)
- `total` (REAL)
- `status` (TEXT, Enum: 'draft', 'sent', 'paid', 'overdue')
- `pdf_path` (TEXT)
- `currency` (TEXT)

### `LineItems`
- `id` (PK, TEXT)
- `invoice_id` (FK -> Invoices.id)
- `description` (TEXT)
- `quantity` (REAL)
- `rate` (REAL)
- `amount` (REAL)

## Design System

**Typography:** Inter (or system-ui) for a clean, modern look.
**Colors:**
- Primary: Navy Blue (`#0F172A`)
- Background: White / Light Gray (`#F8FAFC`)
- Status Badges:
  - **Paid:** Green (`#10B981`, bg: `#D1FAE5`)
  - **Pending / Sent:** Amber (`#F59E0B`, bg: `#FEF3C7`)
  - **Overdue:** Red (`#EF4444`, bg: `#FEE2E2`)
  - **Draft:** Gray (`#6B7280`, bg: `#F3F4F6`)

## Views

1. **Overview Dashboard:**
   - Total Outstanding Balance (Hero metric)
   - Revenue this Month (Bar chart using Chart.js)
   - Recent Invoices table (Date, Number, Client, Amount, Status badge)
2. **Client Directory:**
   - List of clients with Lifetime Value (LTV) calculated from paid invoices.
3. **Invoice History:**
   - Full, sortable table of all invoices. Clickable rows to re-download the PDF.

## ⚠️ Security Requirements
- **Authentication:** Implement user authentication before deploying. No anonymous access to invoice data.
- **Row Level Security (RLS):** Enable Supabase RLS on all tables. Users must only see their own invoices and clients.
- **Encryption:** `payment_details` fields contain sensitive financial data (bank accounts, tax IDs). Enable column-level encryption or use Supabase Vault for these fields. Never store in plaintext in production.
- **PDF Storage:** Store generated invoice PDFs in a **private** storage bucket with signed URLs. Invoices contain business and client financial information.
- **Environment Variables:** All Supabase keys, API URLs, and auth secrets must be stored as environment variables — never hardcoded.
- **Compliance Note:** Users handling client financial data should evaluate their obligations under applicable data protection laws.