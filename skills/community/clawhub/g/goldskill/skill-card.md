## Description:

Provides real-time futures quotes, technical analysis, strategy signals, and related news for gold, silver, crude oil, natural gas, and copper markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tingtt1107](https://clawhub.ai/user/tingtt1107)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to request commodity-market snapshots with price data, technical indicators, news sentiment, and basic buy, sell, or hold strategy signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Yahoo Finance, Stooq, metals.live, Google News, and multiple RSS providers for market data and news.

Mitigation: Install only in environments where those outbound network calls are acceptable, and disclose that third-party data feeds may be unavailable, delayed, or inaccurate.

Risk: Returned headlines and linked news text are untrusted third-party content.

Mitigation: Treat news content as context for analysis only, not as instructions for the agent or as verified facts.

Risk: Commodity strategy signals, stop-loss values, and target levels can be misleading when data feeds fail or market conditions change quickly.

Mitigation: Require human review before trading decisions and present outputs as analytical guidance rather than financial advice.

Risk: The release evidence notes install and robustness risks.

Mitigation: Run the skill in a virtual environment and pin or review dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tingtt1107/skills/goldskill)
- [Publisher profile](https://clawhub.ai/user/tingtt1107)
- [Yahoo Finance chart data](https://query1.finance.yahoo.com/v8/finance/chart/)
- [Stooq quote data](https://stooq.com/q/l/)
- [metals.live spot prices](https://api.metals.live/v1/spot)
- [Google News RSS search](https://news.google.com/rss/search)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text market report suitable for Markdown display]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes current prices, technical indicators, strategy signals, stop-loss and target levels, and recent related headlines when available.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
