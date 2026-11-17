## Description:

Helps agents query JD.com product price history, identify genuine low prices, analyze promotions, set price alerts, and recommend lower-priced similar items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[275254cl-hash](https://clawhub.ai/user/275254cl-hash)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers, ecommerce sellers, and shopping-assistant agents use this skill to review JD.com price history, compare current prices with historical lows, monitor price changes, and decide whether a promotion appears genuine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Price histories, forecasts, or discount assessments may be stale or differ from the live JD.com product page.

Mitigation: Verify current price, seller, availability, and promotion terms on JD.com before purchasing or acting on a recommendation.

Risk: Price alerts and monitoring can create ongoing shopping-assistant behavior that the user may not intend.

Mitigation: Ask the user to confirm the exact product URL or SKU, target price, monitoring scope, and notification preference before setting alerts.

Risk: The requests dependency is not pinned in the artifact metadata.

Mitigation: Install in an isolated environment and pin or review dependencies before using the skill in managed or production agent environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/275254cl-hash/skills/jd-price-history)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance, Configuration]

**Output Format:** [Markdown or plain text price-history analysis with product prices, trend summaries, alert settings, and buying guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Price data is reference-only and should be checked against the current JD.com product page before purchase.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
