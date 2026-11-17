## Description:

InvoiceGuard Pro helps agents extract invoice fields, detect duplicate or suspicious reimbursement records, and draft invoice compliance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yk-global-01](https://clawhub.ai/user/yk-global-01)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations teams use this skill through an agent to review uploaded Chinese invoice files, flag duplicate or suspicious records, and generate internal compliance report drafts.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Invoice authenticity can be overstated when tax verification is not implemented, not configured, or remains unchecked.

Mitigation: Treat tax-status output and compliance reports as internal drafts until a real verification service is configured and unchecked records are clearly reviewed by a human.

Risk: Invoice files can contain sensitive business, tax, buyer, and seller data.

Mitigation: Require explicit approval before sending invoice content to OCR services, tax verification endpoints, Feishu documents, or Feishu tables, and minimize retention of source invoice data.

Risk: Generated compliance reports may be used as proof of authenticity or reimbursement eligibility beyond what the skill can support.

Mitigation: Use generated reports as review aids only, and confirm reimbursement decisions against authoritative tax records and internal finance policy.

## Reference(s):

- [Invoice type and field reference](references/invoice-types.md)
- [Tax verification integration reference](references/tax-api.md)
- [Compliance report template](references/compliance-report.md)
- [Changelog](references/changelog.md)
- [State Taxation Administration invoice verification platform](https://inv-veri.chinatax.gov.cn)
- [ClawHub skill page](https://clawhub.ai/yk-global-01/skills/invoice-guard-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON-like duplicate-check results, shell commands, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require user-provided invoice content and explicit approval before external OCR, tax verification, or Feishu publishing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
