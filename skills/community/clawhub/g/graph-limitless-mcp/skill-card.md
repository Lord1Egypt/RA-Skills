## Description:

Protocol-wide on-chain analytics for Limitless prediction markets on Base, including trader P&L, top traders, market and daily volume history, liquidity events, and raw GraphQL from Limitless subgraphs on The Graph's decentralized network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulieb14](https://clawhub.ai/user/paulieb14)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query Limitless prediction market activity on Base, including market analytics, trader performance, positions, liquidity events, and raw subgraph data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends GraphQL queries and the user's Graph API key to The Graph Gateway.

Mitigation: Use a narrowly scoped or revocable GRAPH_API_KEY and rotate it if exposure is suspected.

Risk: The skill contacts disclosed external endpoints and may be invoked automatically for Limitless prediction market questions.

Mitigation: Install only if the npm package and endpoints are trusted, and disable the skill when automatic Limitless analytics queries are not desired.

Risk: Installing through npx can pull package updates that differ from the reviewed release.

Mitigation: Pin the npm package version when installing or deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paulieb14/skills/graph-limitless-mcp)
- [GitHub repository](https://github.com/PaulieB14/limitless-subgraphs)
- [npm package](https://www.npmjs.com/package/graph-limitless-mcp)
- [Limitless](https://limitless.exchange)
- [The Graph](https://thegraph.com)
- [The Graph API keys](https://thegraph.market/dashboard#api-keys)

## Skill Output:

**Output Type(s):** [Text, Analysis, API Calls, Guidance]

**Output Format:** [Markdown and structured tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GRAPH_API_KEY and returns read-only analytics from disclosed Limitless and The Graph endpoints.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
