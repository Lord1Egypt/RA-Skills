## Description:

Monitor Polymarket prediction markets, fetch current odds, and help set up threshold-based recurring alerts through Slack or similar channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmeir-dev](https://clawhub.ai/user/xmeir-dev)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to find Polymarket markets, report current Yes/No probabilities, and set up recurring threshold alerts. It is useful when a user wants ongoing notification about market odds without repeatedly checking the market manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring cron-based alerts can continue sending Slack notifications after initial setup.

Mitigation: Confirm the exact markets, threshold, check interval, Slack recipient, and removal command before enabling monitoring.

Risk: Market data can include closed or resolved markets with fixed prices.

Mitigation: Check market active and closed status before reporting odds or configuring alerts.

## Reference(s):

- [Polymarket API Reference](references/api.md)
- [Polymarket Gamma API events endpoint](https://gamma-api.polymarket.com/events)
- [Polymarket CLOB markets endpoint](https://clob.polymarket.com/markets/)
- [ClawHub skill page](https://clawhub.ai/xmeir-dev/skills/polymarket-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON market data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cron setup details, market odds, alert thresholds, check frequency, Slack recipient, and cancellation instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
