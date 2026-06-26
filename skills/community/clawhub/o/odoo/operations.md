# Odoo Operating Lanes

Use this file to translate a business request into the correct Odoo lane before suggesting clicks, imports, or API calls.

## Lane 1: Sales and CRM

- Confirm whether the object is lead, opportunity, quotation, sales order, subscription, or invoice.
- Lock company, salesperson, pipeline stage, and draft vs confirmed state before reporting or updating.
- For customer merges, duplicated contacts, or pricing changes, preview downstream documents first.

## Lane 2: Purchasing and Vendor Flows

- Distinguish requisition, purchase order, receipt, vendor bill, and payment.
- Clarify whether the user needs operational status or accounting truth; these often differ.
- For late corrections, prefer a compensating follow-up over rewriting received goods history.

## Lane 3: Inventory and Manufacturing

- Confirm warehouse, locations, routes, lot or serial tracking, and valuation method.
- Stock mistakes often start upstream: wrong product variant, route, unit of measure, or reservation state.
- Fix traceability first. Only then decide whether the correction belongs in inventory adjustment, return, scrap, or manufacturing reversal.

## Lane 4: Accounting and Reconciliation

- Confirm journals, fiscal period, currency, tax scope, and posted vs draft status.
- Never treat an invoice question as only an `account.move` question; payment state and reconciliation matter too.
- When the user wants to "edit" a posted document, explain reversal or correction entry paths first.

## Lane 5: Projects, Services, and Subscriptions

- Separate tasks, timesheets, milestones, helpdesk tickets, and subscription renewals.
- Confirm whether the desired outcome is operational planning, billing, or margin analysis.
- Watch for multi-company and timesheet approval rules before summarizing utilization or profitability.

## Lane 6: Admin, Config, and Automation

- Distinguish user/group changes, server actions, scheduled actions, Studio automation, and external integrations.
- If the task changes behavior globally, identify sandbox or staging first.
- Prefer the simplest native automation that is reviewable and reversible.

## Cross-Lane Defaults

- Say the lane out loud before acting.
- Name the exact business object and state.
- Preview impact before changing records.
- If multiple lanes are involved, sequence them instead of blending them into one unsafe action.
