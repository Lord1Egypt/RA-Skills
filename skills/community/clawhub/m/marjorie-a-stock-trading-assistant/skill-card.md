## Description:

A Stock Trading Assistant helps agents fetch Chinese mainland A-share market data, analyze individual stocks and market sentiment, identify hot sectors, draft trading strategies, and support price alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Chinese A-share market questions by retrieving quotes, index data, sector rankings, and applying documented technical and fundamental analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can provide actionable trading guidance from unauthenticated market data.

Mitigation: Treat outputs as market-analysis assistance, not financial advice, and verify prices, buy/sell ideas, and position sizing against a trusted brokerage or market-data source before acting.

Risk: Alert and watchlist behavior may save user trading interests locally.

Mitigation: Review locally stored alert and watchlist data before sharing or deploying the skill in a shared environment.

## Reference(s):

- [Analysis Method Reference](references/analysis.md)
- [Data Sources API Reference](references/data-sources.md)
- [ClawHub Skill Page](https://clawhub.ai/marjoriebroad/skills/marjorie-a-stock-trading-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis with tables and optional JSON market-data output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market data should include source and fetch time; trading suggestions should include risk warnings.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
