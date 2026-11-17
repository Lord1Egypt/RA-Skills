## Description:

Streams successful Polymarket prediction-market trades on Polygon in real time with USD pricing, market metadata, participant addresses, and transaction details from the Bitquery GraphQL API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[divyn](https://clawhub.ai/user/divyn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, trading analysts, and agent operators use this skill to stream live Polymarket trade activity for dashboards, order-flow monitoring, large-trade detection, market-specific tracking, and on-chain audit trails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Bitquery API token is embedded in the WebSocket URL, so logs, proxies, shell history, debug tooling, or captured network metadata could expose the token.

Mitigation: Run the skill in an isolated environment, keep the token in `BITQUERY_API_KEY`, avoid logging full WebSocket URLs, use a limited token where possible, and rotate the key if exposure is suspected.

Risk: The dependency declaration allows compatible `gql[websockets]` versions rather than pinning an exact package set.

Mitigation: Pin and review dependencies before production deployment, then install from the pinned lockfile or controlled package source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/divyn/skills/polymarket-real-time-trades)
- [Bitquery Polymarket API documentation](https://docs.bitquery.io/docs/examples/polymarket-api/)
- [Bitquery EVM.PredictionTrades field reference](references/graphql-fields.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell snippets; the streaming script prints formatted text trade events.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BITQUERY_API_KEY environment variable and a WebSocket-capable Python dependency.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
