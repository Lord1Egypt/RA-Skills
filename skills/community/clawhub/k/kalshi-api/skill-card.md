## Description:

Read-only Kalshi API skill for market discovery, liquidity checks, and market validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brs999](https://clawhub.ai/user/brs999)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Kalshi market data, inspect exchange status, discover markets and events, review order books and trades, and validate market opportunities without placing orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional KALSHI_BASE_URL override can direct read-only requests to an untrusted endpoint.

Mitigation: Use the default Kalshi production API unless you trust the destination, and review any custom base URL before running commands.

Risk: Market data can be stale, unavailable, or insufficient for trading decisions.

Mitigation: Treat results as discovery and validation inputs only, and verify market details before acting in a separate trading workflow.

## Reference(s):

- [Kalshi API Documentation](https://docs.kalshi.com)
- [Kalshi Production Trade API Base URL](https://api.elections.kalshi.com/trade-api/v2)
- [ClawHub Skill Page](https://clawhub.ai/brs999/skills/kalshi-api)
- [Publisher Profile](https://clawhub.ai/user/brs999)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only API access; commands return endpoint metadata and Kalshi response data as JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
