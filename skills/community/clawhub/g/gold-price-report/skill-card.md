## Description:

Fetches live gold, silver, physical brand gold, and precious-metals futures quote panels for market briefs and scheduled reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plabzzxx](https://clawhub.ai/user/plabzzxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve current precious-metals pricing panels and generate concise market briefs, especially for Chinese-language gold and silver price requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts api-gold.aibuy.cloud for live quote data.

Mitigation: Use it only in environments where outbound access to that disclosed third-party quote API is acceptable.

Risk: Returned prices are third-party market data and may include a copper futures quote alongside precious-metals data.

Mitigation: Treat the report as informational market data, review values before use, and request only the needed sections when copper futures are out of scope.

Risk: The skill may answer in Chinese by default.

Mitigation: Ask for a different language explicitly when the report needs to be delivered in another language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/plabzzxx/skills/gold-price-report)
- [Quote API endpoint](https://api-gold.aibuy.cloud/quoteCenter/realTime.htm)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown report or structured JSON quote data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports related spot products, physical gold brand prices, and futures panels; selected sections can be requested.]

## Skill Version(s):

1.1.1 (source: server release evidence; artifact _meta.json lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
