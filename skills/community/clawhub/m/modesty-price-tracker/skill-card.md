## Description:

Monitor product prices across Amazon, eBay, Walmart, and Best Buy to identify arbitrage opportunities and profit margins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and agent users use this skill to compare marketplace prices, monitor price thresholds, and generate arbitrage or price-history reports for product decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Historical price reports, trend analysis, and predictions may be based on randomly generated simulated history while appearing decision-ready.

Mitigation: Treat historical reports as simulation unless the publisher replaces them with verifiable historical data or clearly labels them as mock output.

Risk: Product queries and search-derived marketplace results are sent to SkillBoss API Hub.

Mitigation: Avoid sensitive product research inputs and install only if sending those queries to SkillBoss is acceptable.

Risk: Arbitrage recommendations depend on extracted prices, seller signals, fee assumptions, and shipping estimates that can be stale or incomplete.

Mitigation: Verify listings, seller reliability, product condition, fees, shipping, taxes, and return windows before acting on purchase or resale decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/modesty-price-tracker)
- [SkillBoss setup guide](https://skillboss.co/skill.md)
- [SkillBoss API Hub endpoint](https://api.skillboss.co/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, shell commands, configuration]

**Output Format:** [Markdown, JSON, CSV, and plain text alert reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may write report files when an output path is provided.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
