## Description:

AR/AP invoice automation for PrecisionLedger that supports aging analysis, follow-up sequencing, payment matching, and collection priority scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting users use this skill to analyze AR/AP aging, draft overdue-payment follow-ups for approval, match payments to open invoices, and prioritize collection activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice, payment, and collections workflows may involve sensitive financial and client data.

Mitigation: Install and use the skill only where sharing the relevant invoice, payment, and collections data with the agent is acceptable.

Risk: Drafted follow-up messages could be sent to clients without required approval.

Mitigation: Keep the stated approval gate in place and require Irfan review before any client communication is sent.

Risk: The skill could be misused to modify accounting records or make final legal, tax, payroll, or dispute decisions.

Mitigation: Use outputs as analysis and briefing material only; do not use the skill to directly modify accounting systems or make final compliance, payroll, tax, legal, or dispute-resolution decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style tables, draft email text, and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce aging reports, payment matching summaries, collection priority matrices, and follow-up drafts that require human review before client use.]

## Skill Version(s):

98.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
