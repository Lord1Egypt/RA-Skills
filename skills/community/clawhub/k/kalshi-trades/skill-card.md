## Description:

Read-only Kalshi OpenAPI scouting skill for market discovery, liquidity checks, market validation, and scanning or ranking Kalshi opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brs999](https://clawhub.ai/user/brs999)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to inspect Kalshi exchange status, discover markets, review events and series, validate individual market tickers, and retrieve read-only trade or order book data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoking the skill contacts the configured Kalshi API host.

Mitigation: Use it only in environments where outbound requests to the intended Kalshi API host are acceptable.

Risk: Changing KALSHI_BASE_URL redirects requests to another server.

Mitigation: Set KALSHI_BASE_URL only to a trusted API host and review the value before running commands.

## Reference(s):

- [Kalshi documentation](https://docs.kalshi.com)
- [Kalshi Trade API v2 endpoint](https://api.elections.kalshi.com/trade-api/v2)
- [ClawHub skill page](https://clawhub.ai/brs999/skills/kalshi-trades)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only API lookup output; no order placement, amendment, cancellation, credential handling, or persistence is described in the security evidence.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
