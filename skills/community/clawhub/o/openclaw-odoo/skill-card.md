## Description: <br>
OpenClaw Odoo connects OpenClaw agents to Odoo 17, 18, and 19 ERP workflows for sales, CRM, purchasing, inventory, projects, HR, fleet, manufacturing, invoicing, calendar, and eCommerce tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuanle96](https://clawhub.ai/user/tuanle96) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Business operators, developers, and OpenClaw users use this skill to query and update Odoo ERP records through agent-assisted commands. It supports broad operational workflows, including smart find-or-create actions for related business records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant an agent broad write, workflow, auto-create, and delete authority over live Odoo business data. <br>
Mitigation: Start in a staging database, use a least-privilege Odoo API user, keep backups and audit logs, and require human confirmation before destructive or state-changing actions. <br>
Risk: Fuzzy smart actions may create missing customers, products, projects, or other dependencies when names do not match existing records. <br>
Mitigation: Require confirmation before smart actions create records and review the skill response for found-versus-created records before proceeding. <br>
Risk: Invoice posting, order confirmation, workflow transitions, website publishing, and deletes can have business impact. <br>
Mitigation: Gate these operations with human approval and restrict API permissions to the specific Odoo models and actions needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tuanle96/openclaw-odoo) <br>
- [Publisher profile](https://clawhub.ai/user/tuanle96) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, inline code, shell commands, configuration snippets, and agent-facing operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Odoo API actions and business-record changes when connected to a live Odoo instance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
