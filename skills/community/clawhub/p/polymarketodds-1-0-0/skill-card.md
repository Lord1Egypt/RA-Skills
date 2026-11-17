## Description:

Query Polymarket prediction markets - check odds, trending markets, search events, track prices and momentum. Includes watchlist alerts, resolution calendar, momentum scanner, and paper trading (simulated, no real money).

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsjustfred](https://clawhub.ai/user/itsjustfred)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query public Polymarket prediction market data, monitor odds and market movement, configure watchlist alerts, review upcoming resolutions, and maintain local paper-trading records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Polymarket's public Gamma API for market data.

Mitigation: Install only where outbound HTTPS requests to gamma-api.polymarket.com are acceptable.

Risk: Watchlists, alert thresholds, simulated positions, and trade history are stored locally under ~/.polymarket.

Mitigation: Review and manage the local JSON files if the machine is shared or if local prediction history should be removed.

Risk: Recurring cron examples can generate repeated API checks and local updates.

Mitigation: Add cron entries only when recurring monitoring is intended, and review the schedule before enabling it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/itsjustfred/skills/polymarketodds-1-0-0)
- [Polymarket](https://polymarket.com)
- [Polymarket API documentation](https://docs.polymarket.com)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style text with command examples and market summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON watchlist and paper portfolio files under ~/.polymarket.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
