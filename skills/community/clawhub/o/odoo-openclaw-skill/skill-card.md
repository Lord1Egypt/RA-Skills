## Description:

Queries Odoo ERP data for salesperson performance, customer analytics, orders, invoices, CRM, accounting, VAT, inventory, and AR/AP reporting, with local report outputs such as WhatsApp cards, PDFs, Excel files, and charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashrf-in](https://clawhub.ai/user/ashrf-in)

### License/Terms of Use:

MIT

## Use Case:

Employees, finance operators, and agents use this skill to query read-only Odoo ERP data and generate evidence-backed financial, sales, CRM, VAT, inventory, and AR/AP reports. It is suited for local report generation after the user provides required company, period, account, breakdown, and output preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Odoo credentials and sensitive financial data.

Mitigation: Configure a dedicated read-only Odoo API account, protect the .env file, and restrict access to locally generated report files.

Risk: Plaintext Odoo URLs or disabled TLS verification can expose credentials or financial data in transit.

Mitigation: Use an HTTPS Odoo URL with valid certificate verification and avoid the --insecure option except in trusted internal environments.

Risk: Dependency drift can change runtime behavior or introduce vulnerabilities.

Mitigation: Review and pin dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ashrf-in/skills/odoo-openclaw-skill)
- [Skill definition](artifact/SKILL.md)
- [Autonomous CFO Engine README](artifact/assets/autonomous-cfo/README.md)
- [Skill metadata](artifact/skill.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands; generated report artifacts may be local PDF, Excel, PNG, chart, or text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Odoo connection credentials plus user-confirmed company, period, account, breakdown, and output-format choices.]

## Skill Version(s):

2.0.5 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
