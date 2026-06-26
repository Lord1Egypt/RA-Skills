## Description: <br>
Query Odoo data including salesperson performance, customer analytics, orders, invoices, CRM, accounting, VAT, inventory, and AR/AP, and generate WhatsApp cards, PDFs, and Excel reports when the user explicitly asks for Odoo data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashrf-in](https://clawhub.ai/user/ashrf-in) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, finance operators, and business users use this skill to query a configured Odoo instance and produce read-only financial, sales, CRM, VAT, inventory, AR/AP, and executive reports with local visual outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive financial data and generates local report files. <br>
Mitigation: Treat generated reports as sensitive files, restrict local access, review reports before sharing, and clean up outputs when no longer needed. <br>
Risk: Odoo credentials are required for operation. <br>
Mitigation: Use a dedicated read-only Odoo API key or user, keep the .env file private, avoid admin credentials, rotate keys periodically, and use HTTPS without the insecure option. <br>
Risk: Read-only behavior is enforced in the client code and could be bypassed by a modified client. <br>
Mitigation: Enforce read-only permissions on the Odoo server side with least-privilege access for the account used by this skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ashrf-in/odoo-reporting) <br>
- [README](README.md) <br>
- [Security Policy](SECURITY.md) <br>
- [Autonomous CFO Engine README](assets/autonomous-cfo/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, shell commands, local PDF reports, Excel workbooks, PNG charts, and WhatsApp card images] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated locally under assets/autonomous-cfo/output/ and depend on the user-configured Odoo instance and selected report format.] <br>

## Skill Version(s): <br>
2.0.7 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
