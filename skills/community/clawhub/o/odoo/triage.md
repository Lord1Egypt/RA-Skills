# Odoo Triage

Use this file when a flow is broken, an import failed, or the user says "Odoo is wrong."

## First Questions

- Which environment: production, staging, local, or unclear?
- Which hosting surface: Odoo Online, Odoo.sh, or self-hosted?
- Which module and business object?
- What changed recently: module install, config tweak, import, access rule, or automation?
- Is the problem data, permissions, workflow state, or integration behavior?

## Common Failure Buckets

| Symptom | First checks |
|---------|--------------|
| Access denied | groups, record rules, company scope, implied groups |
| Wrong numbers | company, timezone, draft/posted states, custom filters |
| Import failures | required fields, identifiers, formatting, duplicate logic |
| Missing inventory | warehouse, routes, reservations, lots, valuation timing |
| Invoice mismatch | journal, taxes, currency, payment state, reconciliation |
| Automation not firing | trigger conditions, scheduler status, logs, domain scope |
| Upgrade broke behavior | module dependencies, views, ACLs, compute fields, deployment surface |

## Triage Sequence

1. Reproduce the issue on the smallest safe example.
2. Identify the exact object, state, and module boundary.
3. Check whether custom modules or Studio rules changed the default behavior.
4. Fix the upstream cause before patching the downstream symptom.
5. Save the incident pattern if it changes the default advice next time.

## Recovery Notes

- Prefer reversible corrections.
- Keep auditability for financial and stock issues.
- If the issue smells like backend repair, slow down and move into the safety ladder before suggesting deeper action.
