## Description:

Scans breaking news and correlates it with active Polymarket markets, probability changes, volume shifts, and large-order movements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnica](https://clawhub.ai/user/cnica)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to connect current news events with related active Polymarket markets. It helps summarize market probability changes, volume movement, and possible large-order activity for informational news-impact analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs may be mistaken for financial advice or relied on without checking the underlying market and news data.

Mitigation: Treat summaries as informational analysis and verify cited news, market status, probability, volume, and trade data before acting on them.

Risk: Broad news phrasing or translated entities can route the skill to loosely related markets.

Mitigation: Confirm entity matching, active-market filtering, and non-English translations before relying on the correlation analysis.

Risk: The skill depends on external data-layer availability for market prices, volumes, and large-order classification.

Mitigation: When enrichment or data access is unavailable, omit unsupported claims and clearly label unclassified addresses or missing data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cnica/skills/polymarket-predictradar-news-impact-skills)
- [Polymarket event pages](https://polymarket.com/event/{slug})

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries with market links, probability changes, volume figures, and large-order notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only informational analysis; probability and volume values must come from the referenced market data sources.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
