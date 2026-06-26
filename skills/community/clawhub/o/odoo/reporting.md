# Odoo Reporting and KPI Scoping

Use this file when the user wants dashboards, summaries, exports, or executive numbers from Odoo.

## Scope Checklist

- Company or companies
- Date range and timezone
- Currency and tax basis
- Draft, posted, canceled, or done states
- Salesperson, team, warehouse, journal, or category cuts
- Output format: answer, table, CSV, spreadsheet, slide, or memo

## Typical Reporting Lenses

| Question type | Common objects | Hidden trap |
|---------------|----------------|-------------|
| Sales pipeline | `crm.lead`, `sale.order` | leads and orders are not interchangeable |
| Revenue | `account.move`, payments, taxes | posted vs unpaid vs cash basis can diverge |
| Inventory | `stock.quant`, `stock.move`, valuation layers | on-hand, forecast, and valuation are different truths |
| Procurement | `purchase.order`, receipts, vendor bills | ordered, received, and billed often differ |
| Service delivery | tasks, timesheets, subscriptions | utilization and billing states may conflict |

## Reporting Defaults

- Start by naming the business definition, not only the technical model.
- Confirm whether the user wants operational truth, accounting truth, or customer-facing truth.
- If a number crosses modules, name each bridge explicitly.
- When the instance is customized, ask for the local status meanings instead of assuming stock Odoo semantics.

## Output Guidance

- Short answer for tactical decisions
- Table with filters for managers
- CSV or spreadsheet for reconciliation
- Memo or deck for executives

If the user asks for "the number," state the assumptions in one line before giving it.
