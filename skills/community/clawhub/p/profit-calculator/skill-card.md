## Description:

Calculate true per-unit profit margins across channels by factoring in COGS, platform fees, shipping costs, ad spend allocation, returns, and overhead to identify which products and channels actually make money.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, founders, and marketplace sellers use this skill to calculate SKU-level and channel-level unit economics. It helps compare DTC, Amazon, TikTok Shop, Walmart, and similar channels using a profit waterfall, sensitivity analysis, and decision flags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be used with confidential ecommerce financial data.

Mitigation: Use only data the user is comfortable sharing in the agent session, and redact sensitive customer, supplier, and account details where possible.

Risk: Marketplace fee schedules and shipping rates can become stale.

Mitigation: Verify current seller documentation, 3PL rate cards, and platform fee notices before finalizing recommendations.

Risk: Incorrect or incomplete COGS, ad attribution, return, or overhead inputs can produce misleading margin guidance.

Mitigation: Validate inputs with the included quality checklist and document assumptions before acting on repricing, channel allocation, or SKU rationalization recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leooooooow/skills/profit-calculator)
- [Output template](references/output-template.md)
- [Platform fee schedule reference](references/fee-schedule-reference.md)
- [Sensitivity analysis guide](references/sensitivity-analysis-guide.md)
- [Quality checklist](assets/quality-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables and concise written analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces per-SKU, per-channel profit waterfall tables, sensitivity analysis, decision flags, and recommended actions when the user provides cost and channel data.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
