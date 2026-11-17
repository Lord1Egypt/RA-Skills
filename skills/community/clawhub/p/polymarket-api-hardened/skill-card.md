## Description:

Query Polymarket prediction markets. Use for questions about prediction markets, betting odds, market prices, event probabilities, or when user asks about Polymarket data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to query live Polymarket public market data, including top markets, search results, market slugs, and event groups. It supports informational probability review and market research, not financial advice or trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Polymarket prices can be mistaken for financial advice or trading instructions.

Mitigation: Present results as public market data and avoid trade execution or financial advice.

Risk: Remote market strings displayed in terminal output can be unsafe or misleading if reused without review.

Mitigation: Review terminal-rendered output before reuse and sanitize remote strings before downstream processing.

Risk: Broad or repeated public API queries can create unnecessary service load.

Mitigation: Limit requests to the market, search term, slug, event, or result count the user explicitly asks for.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/polymarket-api-hardened)
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Faberlens Polymarket API safety report](https://faberlens.ai/explore/polymarket-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell commands, terminal text, and optional JSON API data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries Polymarket public API endpoints without credentials; results can include market questions, outcome prices, volumes, liquidity, status, and dates when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
