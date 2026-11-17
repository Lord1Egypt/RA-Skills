## Description:

Analyze Polymarket prediction markets for trading edges. Pair Cost arbitrage, whale tracking, sentiment analysis, momentum signals, user profile tracking. No execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukebaze](https://clawhub.ai/user/lukebaze)

### License/Terms of Use:


## Use Case:

Developers, analysts, and external users use this skill to evaluate Polymarket markets for analysis-only trading signals, including arbitrage, momentum, wallet activity, sentiment, and recurring market alerts. It does not execute trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring Polymarket monitoring can create persistent cron jobs with ongoing alerts and local state without enough scoping or consent controls.

Mitigation: Before enabling monitor mode, confirm the exact market, duration, state-file location, and alert recipient; set an expiration and remove the cron job when monitoring is finished.

Risk: Alert delivery can use the last active channel, which may send market-monitoring updates to an unintended recipient or venue.

Mitigation: Require an explicit alert channel and recipient for each monitoring job instead of relying on the last-used channel.

Risk: Wallet profile lookups and stored monitoring state can reveal sensitive trading interests or wallet activity even when the underlying data is public.

Mitigation: Treat wallet outputs and state files as sensitive, minimize retention, and avoid sharing them outside the intended analysis context.

## Reference(s):

- [Polymarket API Reference](references/polymarket-api.md)
- [Market Monitoring Setup](references/market-monitoring-setup.md)
- [Pair Cost Arbitrage Strategy](references/pair-cost-arbitrage.md)
- [Momentum Analysis Strategy](references/momentum-analysis.md)
- [Whale Tracking Strategy](references/whale-tracking.md)
- [Sentiment Analysis Strategy](references/sentiment-analysis.md)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Polymarket Data API](https://data-api.polymarket.com)
- [Polymarket CLOB API](https://clob.polymarket.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis-only output; helper scripts may read public Polymarket APIs and maintain local monitoring state.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
