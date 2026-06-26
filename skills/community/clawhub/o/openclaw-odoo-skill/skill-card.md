## Description: <br>
Build or use the Odoo ERP connector for OpenClaw (Sales, CRM, Purchase, Inventory, Projects, HR, Fleet, Manufacturing integration via XML-RPC). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjrhjr](https://clawhub.ai/user/hjrhjr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw agents to Odoo 19 ERP workflows for sales, CRM, purchasing, inventory, invoicing, projects, HR, fleet, manufacturing, calendar, and eCommerce tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Natural-language prompts can trigger broad live changes across business records. <br>
Mitigation: Use a sandbox first, configure a dedicated least-privilege Odoo API user, and require human review before financial, HR, inventory, publish, delete, or receipt-validation actions. <br>
Risk: Smart actions can create missing customers, products, projects, employees, vendors, and related records automatically. <br>
Mitigation: Avoid production auto-create workflows unless confirmation gates are added and reviewed for the affected business process. <br>
Risk: The optional webhook receiver can accept inbound events. <br>
Mitigation: Disable webhooks when not required or protect them with a strong shared secret. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hjrhjr/openclaw-odoo-skill) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Test results](artifact/TEST_RESULTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets plus structured Odoo operation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Odoo connection settings and an API key for live ERP operations] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
