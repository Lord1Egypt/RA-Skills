# Dashboard Spec: Expense Report Pro

This document outlines the companion dashboard for Expense Report Pro. While the skill works flawlessly in chat, the dashboard provides a premium visual interface for managing, organizing, and exporting expenses.

## Core Purpose
"Your agent tracks expenses via chat. Your dashboard is where you review, organize, and generate reports."

## User Interface Requirements

### 1. Main View
* **Data Table:** Sortable and filterable list of all expenses.
  * Columns: Date, Vendor, Category, Amount, Tax, Tip, Currency, Status (Submitted, Approved, Paid).
* **Visuals:**
  * Monthly bar charts showing spending by category.
  * Year-to-date spending line chart.
* **Action Bar:**
  * "Generate PDF Report" button with a date range picker.
  * "Export CSV" button.

### 2. Features
* **Bulk Upload:** Drag-and-drop support for uploading multiple receipt images simultaneously.
* **Inline Editing:** Ability to edit categories, amounts, or vendors directly in the data table.
* **Receipt Viewer:** Clicking a row opens a modal showing the extracted data alongside the original receipt image.

### 3. Design System
* **Theme:** Premium dark theme mimicking high-end FinTech tools.
* **Colors:**
  * Primary actions (buttons, highlights): Teal (`#14b8a6`)
  * Alerts/Accents (errors, over-budget warnings): Orange (`#f97316`)
  * Background: Very dark gray (`#121212`)
* **Layout:** Sidebar navigation for different views (All Expenses, Reports, Budgets, Settings).

---

## ⚠️ SECURITY: Database Schema & Encryption (CRITICAL)

Because this dashboard handles financial data, strict security measures are mandatory.

### 1. Database Schema
Expenses should be stored in a relational database (e.g., Supabase PostgreSQL) if moving beyond the local `expense-log.json`.

```sql
CREATE TABLE expenses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users NOT NULL,
    date DATE NOT NULL,
    vendor VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    amount_cents INTEGER NOT NULL, -- Store as cents to avoid floating point errors
    currency VARCHAR(3) DEFAULT 'USD',
    tax_cents INTEGER DEFAULT 0,
    tip_cents INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'submitted', -- submitted, approved, paid
    is_business BOOLEAN DEFAULT true,
    receipt_image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 2. Row Level Security (RLS)
Ensure users can only access their own data.

```sql
ALTER TABLE expenses ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own expenses"
    ON expenses FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own expenses"
    ON expenses FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own expenses"
    ON expenses FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own expenses"
    ON expenses FOR DELETE
    USING (auth.uid() = user_id);
```

### 3. Encryption Guidance
* **Data at Rest:** The database itself must be encrypted at rest (standard on Supabase/AWS).
* **Sensitive Columns:** If highly sensitive data is stored (e.g., full credit card numbers, which this app *should not* store), use column-level encryption (`pgcrypto`). For standard expense data, RLS + TLS is generally sufficient, but advise users on compliance requirements if they are processing PII.
* **Receipt Images:** Store images in a private S3/Supabase Storage bucket. Generate signed, short-lived URLs for viewing in the dashboard. Never expose receipt images publicly.

### 4. Application Security
* Implement robust authentication (e.g., Supabase Auth).
* Ensure all API endpoints validating data on the server side (never trust the client).
