## Description:

Price Compare helps US shoppers compare product prices across major e-commerce platforms, score result trustworthiness, and choose buying options with warnings for suspicious deals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasye378](https://clawhub.ai/user/lucasye378)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use this skill to compare prices for a named product across major US retailers, evaluate total cost and seller trust signals, and produce buy recommendations with caveats.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Retailer search results can be incomplete, stale, blocked, or affected by browser fallback limitations.

Mitigation: Treat unavailable platforms as incomplete data and verify current prices on retailer pages before acting.

Risk: Low prices, marketplace listings, fake discounts, and unbranded products may be misleading or counterfeit.

Mitigation: Use the skill's trust checklist, anomaly gates, seller checks, price history, and explicit warnings before recommending a purchase.

Risk: The skill produces purchase recommendations and links but does not complete transactions.

Mitigation: Keep final buying decisions and checkout review with the user, including shipping, returns, seller identity, and total cost.

## Reference(s):

- [Price Compare ClawHub Page](https://clawhub.ai/lucasye378/skills/price-compare)
- [ClawHub Skill Homepage](https://clawhub.ai/skills/price-compare)
- [Platform Reference](references/platforms.md)
- [Price Trust Checklist](references/trust-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with comparison tables, recommendations, warnings, price trend notes, and direct links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes trust-scored retailer results and cautions for unavailable, suspicious, or incomplete price data.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
