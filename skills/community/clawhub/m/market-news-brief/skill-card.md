## Description:

Run a local script to fetch broad market news, market tone, index or ETF snapshots, dominant themes, and current headlines for a selected market scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youpele52](https://clawhub.ai/user/youpele52)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market-focused agents use this skill to generate a concise regional or global market news brief before discussing market conditions, sentiment, or macro themes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound Yahoo Finance requests and depends on live market data availability.

Mitigation: Run it in a constrained skill environment and present coverage notes or errors when data is sparse or unavailable.

Risk: The yfinance dependency may change behavior across releases, affecting reproducibility.

Mitigation: Pin or lock yfinance when reproducible output is required.

Risk: Concurrent executions use a small lock file in /tmp, which can delay execution if another run is active or stuck.

Mitigation: Run the skill in the normal constrained environment and monitor or limit concurrent executions if lock acquisition delays occur.

## Reference(s):

- [Yahoo Finance](https://finance.yahoo.com)
- [Market News Brief on ClawHub](https://clawhub.ai/youpele52/skills/market-news-brief)
- [youpele52 ClawHub profile](https://clawhub.ai/user/youpele52)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain-text market brief suitable for Markdown display]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes market scope, tone, snapshots, dominant themes, headlines, timestamps, links, and coverage notes when available.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
