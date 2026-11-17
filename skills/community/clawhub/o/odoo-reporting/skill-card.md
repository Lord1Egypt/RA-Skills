## Description:

Query Odoo data including salesperson performance, customer analytics, orders, invoices, CRM, accounting, VAT, inventory, and AR/AP, and generate WhatsApp cards, PDFs, and Excel reports when the user explicitly requests Odoo data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashrf-in](https://clawhub.ai/user/ashrf-in)

### License/Terms of Use:

MIT

## Use Case:

Employees and developers use this skill to retrieve read-only Odoo ERP data and produce financial, sales, CRM, inventory, VAT, AR/AP, and executive reporting outputs. It supports ledger-based financial statements, ad-hoc comparisons, charts, local PDFs, Excel workbooks, and WhatsApp card images after the user confirms company, period, accounts, breakdowns, and output format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive Odoo financial credentials.

Mitigation: Use a dedicated Odoo API key for a read-only user, keep the .env file out of shared repositories, and restrict file permissions on local credential storage.

Risk: The rpc-call capability can read any Odoo data visible to the configured account.

Mitigation: Grant the Odoo user only the minimum read permissions needed for reporting and review Odoo access logs regularly.

Risk: Disabling TLS verification can expose credentials and financial data in transit.

Mitigation: Require an https:// Odoo URL and do not use the --insecure option in production.

Risk: Dependency safeguards require review before production use.

Mitigation: Install in an isolated Python virtual environment and review or update dependencies before deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ashrf-in/skills/odoo-reporting)
- [README](artifact/README.md)
- [Security policy](artifact/SECURITY.md)
- [Skill instructions](artifact/SKILL.md)
- [Autonomous CFO engine README](artifact/assets/autonomous-cfo/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and locally generated PDF, PNG, Excel, and chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied Odoo credentials and explicit user invocation; report outputs are generated locally under the skill output directory.]

## Skill Version(s):

2.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
