## Description:

Manages work in the huo15/huihuo Odoo system through command scripts for tasks, projects, timesheets, CRM, activities, calendars, knowledge, documents, sales, purchasing, inventory, accounting, HR, briefings, and reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations teams use this skill to work with the company Odoo system from an agent conversation, including personal work management, CRM follow-up, sales, purchasing, inventory, accounting, HR, knowledge, documents, reminders, and daily or weekly briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform major Odoo business changes without enforceable confirmation safeguards.

Mitigation: Use a limited Odoo account and require human confirmation outside the skill before posting payments, posting or canceling invoices, confirming sales or purchase orders, validating stock, approving HR items, deleting records, changing another person's RSVP, or sharing tokenized document links.

Risk: Odoo credentials or API keys can grant access to sensitive company data and actions.

Mitigation: Prefer a revocable Odoo API key, avoid configuring an http:// server, and review the configuration before installing or running the skill.

Risk: Heartbeat or cron polling can repeatedly inspect operational data.

Mitigation: Enable polling only when users understand what data will be checked and how often.

## Reference(s):

- [Command reference](artifact/references/commands.md)
- [Odoo accounting API reference](artifact/references/odoo-accounting-api.md)
- [Odoo activity and calendar API reference](artifact/references/odoo-activity-calendar-api.md)
- [Odoo advanced calendar API reference](artifact/references/odoo-calendar-advanced-api.md)
- [Odoo CRM API reference](artifact/references/odoo-crm-api.md)
- [Odoo HR API reference](artifact/references/odoo-hr-api.md)
- [Odoo knowledge and documents API reference](artifact/references/odoo-knowledge-documents-api.md)
- [Odoo project API reference](artifact/references/odoo-project-api.md)
- [Odoo sales, purchase, and stock API reference](artifact/references/odoo-sales-purchase-stock-api.md)
- [Odoo testing API reference](artifact/references/odoo-testing-api.md)
- [Odoo timesheet API reference](artifact/references/odoo-timesheet-api.md)
- [Odoo todo API reference](artifact/references/odoo-todo-api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown or terminal text with inline shell commands; many scripts also support JSON output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may reflect or modify live Odoo business records depending on the invoked command.]

## Skill Version(s):

1.8.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
