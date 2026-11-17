## Description:

Operate Odoo across CRM, sales, inventory, purchasing, and accounting with module-aware planning, read-before-write checks, and safe execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external operators, developers, and ERP administrators use this skill to plan, inspect, report on, reconcile, import, configure, and safely change Odoo data across live business modules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Odoo operations can affect live CRM, sales, inventory, purchasing, accounting, and customer data.

Mitigation: Use read-only discovery first, preview affected records and side effects, and require explicit confirmation before imports, bulk changes, destructive writes, accounting corrections, inventory fixes, or API writes.

Risk: Reports and KPI answers can be misleading when company, period, timezone, currency, warehouse, fiscal status, or custom state filters are ambiguous.

Mitigation: State assumptions, confirm business scope before giving numbers, and separate operational, accounting, and customer-facing definitions when they differ.

Risk: Direct edits to posted accounting, finalized stock history, or production database records can damage auditability and traceability.

Mitigation: Prefer supported reversal, cancellation, compensating-entry, return, scrap, inventory-adjustment, staging, or rollback workflows before deeper repair paths.

Risk: Credential, export, invoice, payroll, token, or session data could be over-retained in agent memory.

Mitigation: Store only stable operating context in local Odoo memory and do not store passwords, API keys, cookies, personal data exports, invoices, payroll data, or raw accounting dumps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/odoo)
- [Skill homepage](https://clawic.com/skills/odoo)
- [Odoo Skill Definition](artifact/SKILL.md)
- [Odoo Safety Ladder](artifact/safety.md)
- [Odoo Integrations and Automation](artifact/integrations.md)
- [Odoo Reporting and KPI Scoping](artifact/reporting.md)
- [Odoo Hosting Surfaces](artifact/surfaces.md)
- [Common Odoo Models](artifact/models.md)
- [Odoo Triage](artifact/triage.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with optional code blocks, shell commands, configuration notes, tables, CSV or spreadsheet scoping, and written summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs emphasize read-before-write review, scoped assumptions, previews, and explicit confirmation for high-impact Odoo changes.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
