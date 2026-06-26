## Description: <br>
Full-featured Odoo 19 ERP connector for OpenClaw covering Sales, CRM, Purchase, Inventory, Projects, HR, Fleet, Manufacturing, and XML-RPC integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NullNaveen](https://clawhub.ai/user/NullNaveen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and business operators use this skill to let an OpenClaw agent query and manage Odoo ERP records across sales, CRM, purchasing, inventory, invoicing, projects, HR, fleet, manufacturing, calendar, and ecommerce workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad ability to change live Odoo business records. <br>
Mitigation: Use a dedicated least-privilege Odoo API user, test against a staging database first, require explicit human approval for mutating actions, and back up important data. <br>
Risk: Webhook or background polling features can expand the skill's operational surface when enabled. <br>
Mitigation: Keep webhook and background polling disabled unless deliberately configured, secured, and monitored. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/NullNaveen/odoo-connector) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/NullNaveen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration] <br>
**Output Format:** [Human-readable summaries and structured dictionaries from Odoo operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Odoo URL, database, username, and API key; mutating actions can create, update, delete, confirm, post, receive, or publish Odoo records.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
