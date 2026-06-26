## Description: <br>
Full-featured Odoo 19 ERP connector for OpenClaw - Sales, CRM, Purchase, Inventory, Projects, HR, Fleet, Manufacturing (80+ operations, complete Python code included, XML-RPC integration). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NullNaveen](https://clawhub.ai/user/NullNaveen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and business operators use this skill to let an OpenClaw agent connect to Odoo 19 and perform ERP tasks across sales, CRM, purchasing, inventory, invoicing, projects, HR, fleet, manufacturing, calendar, and ecommerce workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Natural-language write commands can directly change live ERP records, including orders, invoices, stock, HR records, and manufacturing data. <br>
Mitigation: Use a least-privilege Odoo API user, start in a test database, and review write actions before execution. <br>
Risk: Smart actions can auto-create customers, vendors, products, projects, employees, and other dependencies when fuzzy matching does not find an existing record. <br>
Mitigation: Limit permissions for the API user and monitor responses that state whether records were found or created. <br>
Risk: The optional webhook server accepts inbound events and should not be exposed without request verification. <br>
Mitigation: Configure a webhook secret before enabling the webhook server and restrict network exposure to trusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NullNaveen/odoo-erp-connector) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, API calls, configuration, guidance] <br>
**Output Format:** [Text summaries and structured dictionaries from Python API calls, with Markdown guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform live Odoo XML-RPC operations and optional webhook processing when configured] <br>

## Skill Version(s): <br>
1.1.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
