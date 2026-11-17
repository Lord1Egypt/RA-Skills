## Description:

Invoice Guard helps agents extract invoice fields, detect duplicate or suspicious reimbursement records, and generate Markdown or Feishu-ready compliance reports for invoice review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiji0802](https://clawhub.ai/user/qiji0802)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations users can use this skill to review uploaded invoices for duplicate reimbursement risk, summarize invoice status, and produce compliance-oriented reports. Official tax verification should only be treated as authoritative when a real tax-platform integration is configured and unchecked records are clearly labeled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated compliance reports may make unchecked invoices appear normal if no real tax-platform verification is connected.

Mitigation: Require a configured tax-platform integration before treating results as official verification, and clearly label records that remain unchecked.

Risk: Invoice data and generated reports can contain sensitive business and financial information.

Mitigation: Use explicit consent before sending invoice data to Feishu or tax services, minimize shared data, and handle generated reports as sensitive business records.

Risk: The server security verdict flags this release for review before installation.

Mitigation: Review and scan the skill before deployment, with special attention to compliance-report wording and external data-sharing behavior.

## Reference(s):

- [Invoice Guard ClawHub listing](https://clawhub.ai/qiji0802/skills/invoice-guard)
- [Invoice type and field reference](references/invoice-types.md)
- [Tax verification platform access notes](references/tax-api.md)
- [Compliance report template](references/compliance-report.md)
- [InvoiceGuard changelog](references/changelog.md)
- [State Taxation Administration invoice verification platform](https://inv-veri.chinatax.gov.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, structured text summaries, Python data structures, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare Feishu/Lark-flavored Markdown and bitable records; official tax checks require configured external services.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
