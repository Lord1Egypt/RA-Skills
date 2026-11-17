## Description:

Track prices, detect deals and manipulation, time purchases, and make informed buying decisions as a consumer or business buyer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and business buyers use this skill to evaluate whether a listed price is fair, track price changes, detect misleading sale tactics, and decide whether to buy now or wait.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store watchlist data, price history, alerts, and purchase decisions locally under ~/price.

Mitigation: Review the local watchlist and history files periodically, and avoid tracking items whose purchase intent or pricing history should not be retained locally.

Risk: Price recommendations may be misleading when source data is stale, incomplete, or based on non-comparable listings.

Mitigation: Use clear product URLs or item names, require cited price-history sources, include total cost, and keep the confidence level visible in each assessment.

## Reference(s):

- [Price Skill on ClawHub](https://clawhub.ai/ivangdavila/skills/price)
- [Retail & Electronics](artifact/retail.md)
- [Travel & Hospitality](artifact/travel.md)
- [B2B & Enterprise Pricing](artifact/b2b.md)
- [Collectibles & Investments](artifact/collectibles.md)
- [Price Manipulation Detection](artifact/manipulation.md)
- [Price Tracking Setup](artifact/tracking.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with structured price assessments, watchlist entries, alerts, and purchase recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain local watchlist, price history, alerts, and purchase logs under ~/price when used for tracking.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
