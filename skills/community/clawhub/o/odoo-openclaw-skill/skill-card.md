## Description: <br>
Query Odoo data including salesperson performance, customer analytics, orders, invoices, CRM, accounting, VAT, inventory, and AR/AP, and generate WhatsApp cards, PDFs, and Excel reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashrf-in](https://clawhub.ai/user/ashrf-in) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and finance teams use this skill to query read-only Odoo ERP data and generate financial, sales, CRM, AR/AP, VAT, inventory, and accounting reports with local PDF, Excel, and WhatsApp-card outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses sensitive financial data and writes local report files that may contain confidential information. <br>
Mitigation: Install it with a dedicated least-privilege read-only Odoo API key, restrict access to intended companies and models, and review or delete generated files after use. <br>
Risk: Ad-hoc metrics or AI-assisted commands can produce misleading financial outputs if unsupported metrics are accepted without review. <br>
Mitigation: Confirm report scope and methodology before use, reject unsupported metrics, and avoid AI commands until the missing OpenClawIntelligence helper and data handling are reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ashrf-in/odoo-openclaw-skill) <br>
- [Autonomous CFO Engine README](artifact/assets/autonomous-cfo/README.md) <br>
- [Skill manifest](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated local report files such as PDF, Excel, and image cards] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Odoo connection settings and writes reports locally.] <br>

## Skill Version(s): <br>
2.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
