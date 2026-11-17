## Description:

Monitor product-level and category-level price gaps, promo shifts, and visible trend signals using browser-collected marketplace data or user-provided price snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and pricing analysts use this skill to compare visible marketplace prices, normalize product or category snapshots, distinguish snapshots from trends, and decide whether to watch, adjust, or gather more data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pricing recommendations may affect margins or competitive positioning if treated as automatic decisions.

Mitigation: Use the skill as decision support, verify margin floors, and review recommended price changes before acting.

Risk: Marketplace pages may be personalized or account-specific when browsed while logged in.

Mitigation: Avoid logging into marketplaces unless account-personalized visibility is needed and the user is comfortable with the agent viewing those pages.

Risk: A single marketplace snapshot can be mistaken for a trend.

Mitigation: Require two observations for a directional signal and three or more time-separated observations before labeling a visible trend.

Risk: Partial or mismatched marketplace coverage can make comparisons misleading.

Mitigation: State platforms, timestamps, search terms, coverage gaps, and normalization choices, and exclude non-comparable listings.

## Reference(s):

- [Output template](references/output-template.md)
- [Pricing data collection guide](references/pricing-data-guide.md)
- [Platform comparison reference](references/platform-comparison-guide.md)
- [Quality checklist](assets/quality-checklist.md)
- [ClawHub skill page](https://clawhub.ai/leooooooow/skills/price-gap-monitor)
- [Publisher profile](https://clawhub.ai/user/leooooooow)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured tables, evidence labels, trend assessment, and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses browser-visible or user-provided marketplace data and labels evidence strength before making pricing recommendations.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
