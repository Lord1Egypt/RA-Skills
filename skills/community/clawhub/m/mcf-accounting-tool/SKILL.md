---
name: Accounting Tool
description: Financial management with invoices, expenses, job costing, P&L reports, and QuickBooks sync — built for AI agents.
author: MCF Agentic
version: 1.0.0
tags: [accounting, invoices, expenses, job-costs, pnl, quickbooks, financial-reports]
pricing: x402 (USDC on Base)
gateway: https://gateway.mcfagentic.com
---

# Accounting Tool

Give your AI agent full control over financial operations. Create and send invoices, log expenses, track job costs, and pull P&L reports — all through simple API calls. Sync everything to QuickBooks when you need it in your traditional accounting stack. Ideal for agents managing client billing, tracking project profitability, or automating month-end reporting without touching a spreadsheet.

## Authentication

All endpoints require x402 payment (USDC on Base L2). Send a request without payment to receive pricing info in the 402 response.

## Endpoints

| Method | Path | Price | Description |
|--------|------|-------|-------------|
| GET | /api/accounting/stats | $0.001 | Financial overview |
| GET | /api/accounting/invoices | $0.001 | List invoices |
| POST | /api/accounting/invoices | $0.01 | Create invoice |
| GET | /api/accounting/invoices/:id | $0.001 | Get invoice details |
| PATCH | /api/accounting/invoices/:id/send | $0.05 | Send invoice |
| PATCH | /api/accounting/invoices/:id/pay | $0.01 | Mark invoice paid |
| GET | /api/accounting/expenses | $0.001 | List expenses |
| POST | /api/accounting/expenses | $0.01 | Create expense |
| GET | /api/accounting/job-costs | $0.001 | List job costs |
| POST | /api/accounting/job-costs | $0.01 | Create job cost entry |
| GET | /api/accounting/job-costs/summary | $0.01 | Job cost summary |
| GET | /api/accounting/reports/pnl | $0.05 | P&L report |
| GET | /api/accounting/reports/revenue-by-month | $0.05 | Revenue by month |
| GET | /api/accounting/reports/expenses-by-category | $0.05 | Expenses by category |
| POST | /api/accounting/quickbooks/sync | $0.10 | Sync with QuickBooks |
| GET | /api/accounting/quickbooks/sync-log | $0.001 | QuickBooks sync log |
