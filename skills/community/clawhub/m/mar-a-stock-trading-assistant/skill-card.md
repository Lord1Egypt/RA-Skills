## Description:

A Stock Trading Assistant helps agents retrieve mainland China A-share market data and produce quotes, technical and fundamental analysis, market sentiment summaries, sector views, strategy suggestions, and price-alert guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer mainland China A-share stock questions, including stock quotes, index and sector analysis, trading strategy framing, and alert follow-up. It is scoped to Shanghai and Shenzhen A-share tickers and should be used as informational support, not as a broker or execution system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce actionable trading guidance from live market data fetched over unauthenticated HTTP sources.

Mitigation: Treat outputs as informational only and verify prices, recommendations, and order decisions through a trusted broker or HTTPS market-data source before acting.

Risk: Price-alert watchlists may persist locally when alerts are used.

Mitigation: Review and remove local watchlist entries that are no longer needed, especially on shared or managed systems.

## Reference(s):

- [Individual Stock Analysis Method Reference](references/analysis.md)
- [Data Source API Reference](references/data-sources.md)
- [ClawHub Skill Page](https://clawhub.ai/marjoriebroad/skills/mar-a-stock-trading-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with optional tables, shell command examples, and JSON from the stock-fetch script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market-data outputs are expected to cite the data source and retrieval time.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
