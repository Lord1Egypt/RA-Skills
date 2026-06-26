# Common Odoo Models

Use this map to avoid mixing business objects that sound similar but behave differently.

| Domain | Common model | Notes |
|--------|--------------|-------|
| Contacts | `res.partner` | customers, vendors, companies, contacts, addresses |
| Leads and opportunities | `crm.lead` | pipeline object for CRM, not a customer record |
| Quotations and sales orders | `sale.order` | draft quotation and confirmed order share the same model with different states |
| Products | `product.template` / `product.product` | template vs variant matters for pricing, stock, and attributes |
| Purchase orders | `purchase.order` | vendor flow object, separate from bills and receipts |
| Invoices and bills | `account.move` | one model covers invoices, bills, and journal entries with type/state context |
| Payments | `account.payment` | payment flow and reconciliation state may matter more than the invoice itself |
| Inventory moves | `stock.move` | demand and movement layer, not on-hand snapshot |
| On-hand stock | `stock.quant` | current quantity by location, lot, package, owner |
| Pickings | `stock.picking` | operational document for receipts, deliveries, transfers |
| Manufacturing | `mrp.production` | work order and consumption links can matter |
| Projects and tasks | `project.project` / `project.task` | billing or timesheets often live elsewhere too |
| Timesheets | `account.analytic.line` | services and margin reporting usually flow through here |

## Model Rules

- Verify the state field before assuming lifecycle semantics.
- Check company and access context on any cross-company analysis.
- If custom modules are present, record the local overrides in `~/odoo/modules.md`.
- When in doubt, describe the business object first and the model second.
