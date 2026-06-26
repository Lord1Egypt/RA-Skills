## Description: <br>
Operate Odoo across CRM, sales, inventory, purchasing, and accounting with module-aware planning, read-before-write checks, and safe execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business users use this skill to plan and execute safer Odoo reporting, imports, integrations, configuration, reconciliation, and operational changes across live ERP environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Guidance may affect live ERP records, including accounting, inventory, purchasing, sales, and customer operations. <br>
Mitigation: Use least-privileged Odoo accounts, prefer staging or read-only review for risky work, and require explicit approval before imports, bulk edits, accounting changes, inventory corrections, or automations. <br>
Risk: Persistent Odoo memory can retain operating context that becomes stale or too broad for future tasks. <br>
Mitigation: Decide when the skill may activate, periodically review the ~/odoo/ memory files, and avoid storing passwords, tokens, session cookies, raw exports, invoices, payroll data, or copied ledgers. <br>
Risk: Odoo reports can be misleading when company, period, timezone, currency, warehouse, fiscal status, or custom workflow states are not scoped. <br>
Mitigation: Confirm reporting scope and business definitions before giving numbers, and state key assumptions when producing KPI summaries or exports. <br>


## Reference(s): <br>
- [ClawHub Odoo skill page](https://clawhub.ai/ivangdavila/odoo) <br>
- [Odoo skill homepage](https://clawic.com/skills/odoo) <br>
- [Setup guide](artifact/setup.md) <br>
- [Safe writes and approval ladder](artifact/safety.md) <br>
- [API, imports, and automation choices](artifact/integrations.md) <br>
- [Hosting surface map](artifact/surfaces.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with optional inline commands, code snippets, tables, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include review checklists, scoped reporting assumptions, import plans, API payload guidance, and approval steps before risky Odoo changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
