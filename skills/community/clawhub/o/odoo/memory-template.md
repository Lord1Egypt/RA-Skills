# Memory Template — Odoo

Create `~/odoo/memory.md` with this structure:

```markdown
# Odoo Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Environment
- Instance: production | staging | local
- Companies:
- Odoo version:
- Main modules:

## Operating Rules
- Read/write boundary:
- Approval boundary:
- Preferred interfaces: UI | import | XML-RPC | JSON-RPC | mixed

## Customization Notes
- Custom modules:
- Studio fields:
- Renamed states or workflows:

## Reporting Defaults
- Timezone:
- Currency:
- Standard status filters:
- Preferred output:

## Notes
- Durable context only

---
*Updated: YYYY-MM-DD*
```

## Optional companion files

- `~/odoo/instances.md` for per-instance URLs, auth lanes, and owners
- `~/odoo/modules.md` for custom fields and model overrides
- `~/odoo/incidents.md` for failed imports, broken automations, or audit-sensitive corrections

## Key Principles

- Store stable operating facts, not temporary tickets
- Prefer natural language notes over config-like keys outside the status block
- Never store credentials, exports, invoices, payroll data, or copied ledgers
- Update `last` every time the skill is used
- Keep the memory useful for the next real Odoo task, not exhaustive
