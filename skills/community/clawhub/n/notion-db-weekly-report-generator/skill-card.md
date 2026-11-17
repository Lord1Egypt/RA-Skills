## Description:

Converts Notion-style task records into weekly report Markdown and reserves premium upgrade hooks for trend analysis and management summary automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wingogx](https://clawhub.ai/user/wingogx)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to turn Notion-style task records into a weekly status report with summary statistics, highlights, risks, and upgrade guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal output includes monetization metadata and a payment link.

Mitigation: Use the skill only where payment-link behavior is desired, and review payment URL configuration before sharing generated reports.

Risk: Task record text is rendered into Markdown output.

Mitigation: Avoid rendering reports from untrusted task records in permissive Markdown viewers without sanitizing or escaping the record content.

Risk: The package includes billing-contract documentation that is broader than weekly report generation.

Mitigation: Review the bundled billing-contract reference during installation to confirm the monetization scope is acceptable.

## Reference(s):

- [SkillPay API Contract](artifact/references/skillpay-api-contract.md)
- [ClawHub Skill Page](https://clawhub.ai/wingogx/skills/notion-db-weekly-report-generator)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [JSON object containing report Markdown, statistics, highlight and risk lists, and upgrade metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free-tier output includes premium availability, price, feature list, and a payment URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
