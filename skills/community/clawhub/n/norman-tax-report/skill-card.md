## Description:

Review and manage German tax reports including VAT (Umsatzsteuer), income tax prepayments, and Finanzamt submissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanlee000](https://clawhub.ai/user/stanlee000)

### License/Terms of Use:


## Use Case:

External Norman Finance users use this skill to review German tax reports, inspect VAT deadlines and tax settings, preview Finanzamt submissions, and file reports through ELSTER after explicit confirmation.

### Deployment Geography for Use:

Germany

## Known Risks and Mitigations:

Risk: The connected MCP server can access tax reports, VAT settings, and filing actions.

Mitigation: Install only if you use Norman Finance for German tax reporting and accept that access scope.

Risk: ELSTER filing is high impact and tax submissions are irreversible.

Mitigation: Review the Finanzamt preview carefully and submit only after explicit user confirmation.

Risk: Missed or misunderstood VAT filing deadlines may affect tax compliance.

Mitigation: Use the skill to check upcoming VAT deadlines and confirm obligations against current tax records.

## Reference(s):

- [Norman Finance homepage](https://norman.finance)
- [ClawHub skill listing](https://clawhub.ai/stanlee000/skills/norman-tax-report)
- [Publisher profile](https://clawhub.ai/user/stanlee000)

## Skill Output:

**Output Type(s):** [Guidance, Text, API Calls]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the Norman Finance MCP server to retrieve tax report data, generate previews, validate tax numbers, and submit only after explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
