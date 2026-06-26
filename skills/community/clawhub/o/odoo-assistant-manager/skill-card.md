## Description: <br>
Odoo ERP via XML-RPC -- sales, web orders, stock, products (CLI). Optional Discuss listener. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crbwi](https://clawhub.ai/user/crbwi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store operators and agents use this skill to inspect Odoo sales, web orders, stock, products, order details, and event registrations from the terminal. It can also run an optional Odoo Discuss listener that polls messages and invokes the same management commands when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional Odoo Discuss listener can make live ERP changes from chat messages without clear user or channel authorization controls. <br>
Mitigation: Avoid running the listener in production until allowed users and channels, confirmations for write actions, URL restrictions, HTTPS validation, and PII redaction or authorization are added. <br>
Risk: The skill performs privileged Odoo operations against sales, stock, products, orders, and events. <br>
Mitigation: Install only if the publisher is trusted, use a dedicated least-privilege Odoo account, and test against a non-production database first. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/crbwi/odoo-assistant-manager) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Skill manifest](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with terminal commands and summarized command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ODOO_URL, ODOO_DB, ODOO_USER, and ODOO_PASSWORD or ODOO_PASS; the optional listener also requires ODOO_BOT_PARTNER_ID.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact SKILL.md and skill.json state 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
