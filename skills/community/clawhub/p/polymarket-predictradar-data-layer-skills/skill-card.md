## Description:

Shared Polymarket and prediction-market data access layer. Use this skill whenever another skill or task needs trader positions, trade history, market metadata, leaderboard data, win-rate or PnL statistics, or any other read-only market intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnica](https://clawhub.ai/user/cnica)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as a shared read-only access layer for Polymarket market metadata, trader positions, trade history, leaderboards, PnL statistics, SQL previews, and larger stream exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An API key could be forwarded to an untrusted stream URL.

Mitigation: Validate stream URL origins before sending API keys.

Risk: Invalid TLS certificates may be accepted by parts of the implementation.

Mitigation: Require valid TLS verification before production or multi-user use.

Risk: Unsafe SQL construction may allow malformed or unintended queries.

Mitigation: Validate or parameterize SQL inputs and keep queries read-only.

Risk: Local caches may retain wallet and trader analytics longer than intended.

Mitigation: Set a cache retention policy and clear cached data when freshness or privacy requirements demand it.

## Reference(s):

- [Fallback Queries](references/fallback-queries.md)
- [Polymarket Shared Analytics Fields / API Field Reference](references/table-schema.md)
- [PredicTradar MCP Server](https://api.predictradar.ai/api/mcp/v2)
- [Polymarket Data API](https://data-api.polymarket.com)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Polymarket CLI](https://github.com/Polymarket/polymarket-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript, SQL, shell command, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API calls, read-only SQL previews, streamed export guidance, and local cache usage guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
