## Description:

This skill helps an agent query Polymarket public APIs for prediction-market odds, market details, trending markets, sports schedules, live or in-play markets, series, tournaments, and event data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amurtiger01](https://clawhub.ai/user/amurtiger01)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to look up public Polymarket market data, including implied probabilities, volumes, schedules, event details, and current prices. It is suited for answering market-data questions, not for placing trades or providing financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send Polymarket search terms, market IDs, event IDs, and selected topics to Polymarket public APIs.

Mitigation: Avoid using the skill for private or sensitive intent; use it only for public market lookup questions.

Risk: Prediction-market prices are market-implied probabilities that can change quickly and may be delayed by seconds to minutes.

Mitigation: Present results as current market data, include timing context when useful, and verify important real-world claims against primary sources.

Risk: The skill does not provide a real-time score feed, and server security guidance notes that one live-market command appears to have a Python bug.

Mitigation: Use sports-specific sources for live scores and validate live-market command output before relying on it.

## Reference(s):

- [Polymarket API Reference](references/api_reference.md)
- [ClawHub Skill Page](https://clawhub.ai/amurtiger01/skills/polymarket-query)
- [Project Homepage](https://github.com/Amurtiger01/polymarket-skill)
- [Polymarket](https://polymarket.com/)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Polymarket CLOB API](https://clob.polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown prose with summarized command output and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled query scripts print human-readable market, odds, schedule, sports metadata, series, and tournament results from public API responses.]

## Skill Version(s):

1.6.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
