---
name: oo-quickbooks
description: "QuickBooks Online (quickbooks.intuit.com). Use this skill for ANY QuickBooks Online request — reading, creating, updating, and deleting data. Whenever a task involves QuickBooks Online, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "QuickBooks Online"
  author: "OOMOL"
  version: "1.0.2"
  services: ["quickbooks"]
  icon: "https://static.oomol.com/logo/third-party/quickbooks.svg"
---

# QuickBooks Online

Operate **QuickBooks Online** through your OOMOL-connected account. This skill calls the `quickbooks` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected QuickBooks Online. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "quickbooks" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "quickbooks" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `batch` — Run up to 30 operations in one request. Each item is either a read-only query or a create, update or delete of one entity. Items do not roll back each other when one fails. [destructive]
- `create_account` — Create a account. [write]
- `create_bill` — Create a bill. [write]
- `create_bill_payment` — Create a bill payment. [write]
- `create_credit_memo` — Create a credit memo. [write]
- `create_credit_term` — Create a credit term. [write]
- `create_customer` — Create a customer. [write]
- `create_department` — Create a department. [write]
- `create_deposit` — Create a deposit. [write]
- `create_employee` — Create a employee. [write]
- `create_estimate` — Create a estimate. [write]
- `create_invoice` — Create an invoice for a customer from one or more sales lines. [write]
- `create_journal_code` — Create a journal code. [write]
- `create_journal_entry` — Create a journal entry. [write]
- `create_payment` — Record a customer payment, optionally applying it to specific invoices. [write]
- `create_payment_method` — Create a payment method. [write]
- `create_product` — Create a product or service. [write]
- `create_purchase` — Create a purchase (expense, check or credit card charge). [write]
- `create_purchase_order` — Create a purchase order. [write]
- `create_record` — Create a record of any supported entity by name. [write]
- `create_refund_receipt` — Create a refund receipt. [write]
- `create_sales_receipt` — Create a sales receipt. [write]
- `create_tax_agency` — Create a tax agency. [write]
- `create_time_activity` — Create a time activity. [write]
- `create_transfer` — Create a transfer. [write]
- `create_vendor` — Create a vendor. [write]
- `create_vendor_credit` — Create a vendor credit. [write]
- `delete_account` — Deactivate a account by setting Active to false. QuickBooks does not delete this kind of record. [destructive]
- `delete_attachment` — Permanently delete an attachment. [destructive]
- `delete_bill` — Permanently delete a bill. This cannot be undone. [destructive]
- `delete_bill_payment` — Permanently delete a bill payment. This cannot be undone. [destructive]
- `delete_credit_memo` — Permanently delete a credit memo. This cannot be undone. [destructive]
- `delete_credit_term` — Deactivate a credit term by setting Active to false. QuickBooks does not delete this kind of record. [destructive]
- `delete_customer` — Deactivate a customer by setting Active to false. QuickBooks does not delete this kind of record. [destructive]
- `delete_department` — Deactivate a department by setting Active to false. QuickBooks does not delete this kind of record. [destructive]
- `delete_deposit` — Permanently delete a deposit. This cannot be undone. [destructive]
- `delete_employee` — Deactivate a employee by setting Active to false. QuickBooks does not delete this kind of record. [destructive]
- `delete_estimate` — Permanently delete a estimate. This cannot be undone. [destructive]
- `delete_invoice` — Permanently delete an invoice. This cannot be undone; void the invoice instead to keep a record. [destructive]
- `delete_journal_entry` — Permanently delete a journal entry. This cannot be undone. [destructive]
- `delete_payment` — Permanently delete a payment. This cannot be undone. [destructive]
- `delete_payment_method` — Deactivate a payment method by setting Active to false. QuickBooks does not delete this kind of record. [destructive]
- `delete_product` — Deactivate a product or service by setting Active to false. QuickBooks does not delete this kind of record. [destructive]
- `delete_purchase` — Permanently delete a purchase (expense, check or credit card charge). This cannot be undone. [destructive]
- `delete_purchase_order` — Permanently delete a purchase order. This cannot be undone. [destructive]
- `delete_record` — Delete a record of any supported entity by name. Entities QuickBooks cannot delete are deactivated instead. [destructive]
- `delete_refund_receipt` — Permanently delete a refund receipt. This cannot be undone. [destructive]
- `delete_sales_receipt` — Permanently delete a sales receipt. This cannot be undone. [destructive]
- `delete_time_activity` — Permanently delete a time activity. This cannot be undone. [destructive]
- `delete_transfer` — Permanently delete a transfer. This cannot be undone. [destructive]
- `delete_vendor` — Deactivate a vendor by setting Active to false. QuickBooks does not delete this kind of record. [destructive]
- `delete_vendor_credit` — Permanently delete a vendor credit. This cannot be undone. [destructive]
- `get_account` — Get one account by ID.
- `get_attachment` — Get an attachment's metadata by ID.
- `get_attachment_download_url` — Get a temporary URL to download an attachment's file.
- `get_bill` — Get one bill by its ID.
- `get_bill_payment` — Get one bill payment by its ID.
- `get_changes` — List records of the given entities that changed since a point in time (change data capture). QuickBooks looks back at most 30 days and returns at most 1000 records per call.
- `get_company_info` — Get the connected company's profile: name, legal name, address, fiscal year start and country.
- `get_credit_memo` — Get one credit memo by its ID.
- `get_credit_term` — Get one credit term by its ID.
- `get_customer` — Get one customer by ID, including its current SyncToken.
- `get_department` — Get one department by its ID.
- `get_deposit` — Get one deposit by its ID.
- `get_employee` — Get one employee by its ID.
- `get_estimate` — Get one estimate by its ID.
- `get_exchange_rate` — Get the exchange rate from a currency to the company's home currency.
- `get_invoice` — Get one invoice by ID, including its lines, balance and current SyncToken.
- `get_journal_code` — Get one journal code by its ID.
- `get_journal_entry` — Get one journal entry by its ID.
- `get_payment` — Get one payment by ID, including the invoices it was applied to.
- `get_payment_method` — Get one payment method by its ID.
- `get_preferences` — Get the company preferences: accounting, sales, tax, currency and other settings.
- `get_product` — Get one product or service by its ID.
- `get_purchase` — Get one purchase (expense, check or credit card charge) by its ID.
- `get_purchase_order` — Get one purchase order by its ID.
- `get_record` — Get one record of any supported entity by name and ID.
- `get_refund_receipt` — Get one refund receipt by its ID.
- `get_report` — Run any QuickBooks report. Use `parameters` for report-specific options such as customer, vendor or account filters.
- `get_sales_receipt` — Get one sales receipt by its ID.
- `get_tax_agency` — Get one tax agency by its ID.
- `get_tax_code` — Get one tax code by its ID.
- `get_tax_rate` — Get one tax rate by its ID.
- `get_time_activity` — Get one time activity by its ID.
- `get_transfer` — Get one transfer by its ID.
- `get_vendor` — Get one vendor by its ID.
- `get_vendor_credit` — Get one vendor credit by its ID.
- `list_accounts` — List accounts from the chart of accounts, optionally filtered by type or name.
- `list_attachments` — List attachments, optionally only those linked to one record.
- `list_bill_payments` — List bill payments, optionally filtered.
- `list_bills` — List bills, optionally filtered.
- `list_budgets` — List budgets, optionally filtered.
- `list_classes` — List classs, optionally filtered.
- `list_credit_memos` — List credit memos, optionally filtered.
- `list_credit_terms` — List credit terms, optionally filtered.
- `list_currencies` — List currencys, optionally filtered.
- `list_customers` — List customers, optionally filtered by name or active status.
- `list_departments` — List departments, optionally filtered.
- `list_deposits` — List deposits, optionally filtered.
- `list_employees` — List employees, optionally filtered.
- `list_estimates` — List estimates, optionally filtered.
- `list_invoices` — List invoices, optionally filtered by customer, number, date range or open balance.
- `list_journal_codes` — List journal codes, optionally filtered.
- `list_journal_entries` — List journal entrys, optionally filtered.
- `list_payment_methods` — List payment methods, optionally filtered.
- `list_payments` — List customer payments, optionally filtered by customer or date range.
- `list_products` — List product or services, optionally filtered.
- `list_purchase_orders` — List purchase orders, optionally filtered.
- `list_purchases` — List purchase (expense, check or credit card charge)s, optionally filtered.
- `list_records` — List records of any supported entity by name. Prefer the entity-specific list actions.
- `list_refund_receipts` — List refund receipts, optionally filtered.
- `list_sales_receipts` — List sales receipts, optionally filtered.
- `list_tax_agencies` — List tax agencys, optionally filtered.
- `list_tax_codes` — List tax codes, optionally filtered.
- `list_tax_rates` — List tax rates, optionally filtered.
- `list_time_activities` — List time activitys, optionally filtered.
- `list_transfers` — List transfers, optionally filtered.
- `list_vendor_credits` — List vendor credits, optionally filtered.
- `list_vendors` — List vendors, optionally filtered.
- `ping` — Check that the connection works by reading the company profile.
- `update_attachment` — Update an attachment's metadata, such as its note or file name. [write]
- `update_bill` — Update a bill. With the default sparse update only the supplied fields change. [write]
- `update_bill_payment` — Update a bill payment. With the default sparse update only the supplied fields change. [write]
- `update_credit_memo` — Update a credit memo. With the default sparse update only the supplied fields change. [write]
- `update_credit_term` — Update a credit term. With the default sparse update only the supplied fields change. [write]
- `update_customer` — Update a customer. Customers cannot be deleted in QuickBooks; set `additional_fields.Active` to false to deactivate one. [write]
- `update_department` — Update a department. With the default sparse update only the supplied fields change. [write]
- `update_deposit` — Update a deposit. With the default sparse update only the supplied fields change. [write]
- `update_employee` — Update a employee. With the default sparse update only the supplied fields change. [write]
- `update_estimate` — Update a estimate. With the default sparse update only the supplied fields change. [write]
- `update_invoice` — Update an invoice. With the default sparse update only the supplied fields change; a supplied `lines` array replaces the invoice's lines. [write]
- `update_journal_code` — Update a journal code. With the default sparse update only the supplied fields change. [write]
- `update_journal_entry` — Update a journal entry. With the default sparse update only the supplied fields change. [write]
- `update_payment` — Update a payment. With the default sparse update only the supplied fields change. [write]
- `update_product` — Update a product or service. With the default sparse update only the supplied fields change. [write]
- `update_purchase` — Update a purchase (expense, check or credit card charge). With the default sparse update only the supplied fields change. [write]
- `update_purchase_order` — Update a purchase order. With the default sparse update only the supplied fields change. [write]
- `update_record` — Update a record of any supported entity by name. [write]
- `update_refund_receipt` — Update a refund receipt. With the default sparse update only the supplied fields change. [write]
- `update_sales_receipt` — Update a sales receipt. With the default sparse update only the supplied fields change. [write]
- `update_time_activity` — Update a time activity. With the default sparse update only the supplied fields change. [write]
- `update_transfer` — Update a transfer. With the default sparse update only the supplied fields change. [write]
- `update_vendor` — Update a vendor. With the default sparse update only the supplied fields change. [write]
- `update_vendor_credit` — Update a vendor credit. With the default sparse update only the supplied fields change. [write]
- `upload_attachment` — Upload a file to QuickBooks, optionally attached to a transaction or other record. [write]
- `void_invoice` — Void an invoice. QuickBooks keeps the record but zeroes its amounts, so the invoice no longer counts toward balances. [destructive]
- `void_payment` — Void a payment. QuickBooks keeps the record but zeroes its amounts. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change QuickBooks Online state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — QuickBooks Online is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/quickbooks
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- QuickBooks Online homepage: https://quickbooks.intuit.com
- API documentation: https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account
