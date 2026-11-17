# Pressmark document types

Author: Daniel Hallman

These examples describe common templates. Use the document type accepted by the connected server.

## Invoices

- `invoice`: Itemized invoice with payment terms and bank or wire instructions.
- `invoice_freelance`: Invoice for hours, day rates, or project milestones.
- `invoice_construction`: Construction billing with retainage, work progress, materials, and labor fields.
- `invoice_medical`: Patient or insurance statement with procedure codes, diagnosis codes, copays, and deductibles. These fields do not establish compliance with a billing standard.
- `invoice_saas`: Subscription invoice with plan, seat, and usage charges.
- `invoice_minimal`: Monochrome invoice with a compact layout.
- `proforma_invoice`: Preliminary invoice with goods values, tariff codes, country of origin, and Incoterms.

## Estimates and quotes

- `estimate`: Estimated labor and material costs with an expiry date.
- `quotation_tender`: Quote with milestones, deliverables, and fixed prices.

## Orders and payments

- `receipt`: Payment record with a transaction reference and method.
- `purchase_order`: Order with a purchase order number and delivery instructions.
- `packing_slip`: Shipment contents, dimensions, weights, and handling instructions, without prices.
- `credit_note`: Credit adjustment that references the original invoice and reason. It does not send a refund.

## Contracts and real estate

- `agreement` / `agreement_sow`: Agreement or statement of work with scope, milestones, and signature blocks.
- `nda`: Non-disclosure agreement with confidentiality terms.
- `residential_lease`: Lease with rent, deposit, tenant terms, and available jurisdiction-specific notices.
- `commercial_nnn_lease`: Commercial lease with base rent and common area maintenance charges.
- `rent_roll`: Tenant and unit schedule with area, rent, and lease dates.
- `closing_settlement_statement`: Buyer and seller charges, credits, and cash due at closing.
