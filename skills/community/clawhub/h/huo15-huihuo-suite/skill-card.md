## Description: <br>
辉火套件ERP lets an agent help users operate the 火一五/辉火云 Odoo ERP system for to-dos, projects, timesheets, CRM, activities, calendar events, knowledge articles, documents, sales, purchasing, inventory, and daily or weekly briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and business operators use this skill to ask an agent to read, create, update, and summarize work records in a company Odoo ERP account. It is intended for operational workflows such as task tracking, project work, sales and purchase order handling, inventory checks, meetings, documents, and CRM follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores live Odoo credentials and can operate a company ERP account. <br>
Mitigation: Use a revocable Odoo API key with the least privileges needed, keep ~/.huo15/tools.md out of backups and git, and install only when the publisher is trusted. <br>
Risk: The skill exposes broad business-changing actions such as order confirmation, bills, invoices, cancellations, stock validations, and task updates. <br>
Mitigation: Manually verify record IDs and business details before allowing the agent to run commands that create, confirm, cancel, validate, or otherwise modify ERP records. <br>
Risk: Server security review marked the release suspicious because confirmation and scope checks are not consistent across sensitive operations. <br>
Mitigation: Require explicit user confirmation for destructive, financial, inventory, or bulk state-changing actions before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-huihuo-suite) <br>
- [Command reference](references/commands.md) <br>
- [Odoo activity and calendar API reference](references/odoo-activity-calendar-api.md) <br>
- [Odoo advanced calendar API reference](references/odoo-calendar-advanced-api.md) <br>
- [Odoo CRM API reference](references/odoo-crm-api.md) <br>
- [Odoo knowledge and documents API reference](references/odoo-knowledge-documents-api.md) <br>
- [Odoo project API reference](references/odoo-project-api.md) <br>
- [Odoo sales, purchase, and stock API reference](references/odoo-sales-purchase-stock-api.md) <br>
- [Odoo timesheet API reference](references/odoo-timesheet-api.md) <br>
- [Odoo to-do API reference](references/odoo-todo-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Text] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python scripts and saved or environment-provided Odoo credentials; several commands can change live ERP records.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
