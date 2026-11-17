## Description:

Read-only Kalshi OpenAPI scouting skill for market discovery, liquidity checks, and market validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brs999](https://clawhub.ai/user/brs999)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and analysts use this skill to scout Kalshi markets, check exchange status, inspect events and series, and review orderbook or trade data before using a separate reviewed workflow for execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for an order-entry or account-management tool.

Mitigation: Use it only for read-only market scouting and route any paper or real trading workflow to a separate reviewed execution skill.

Risk: The skill makes network requests to Kalshi and prints returned market data.

Mitigation: Install it only in environments where read-only Kalshi API access and display of returned market data are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brs999/skills/kalshi-trade)
- [Kalshi Trade API base endpoint](https://api.elections.kalshi.com/trade-api/v2)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; CLI responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and makes read-only GET requests to Kalshi OpenAPI endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
