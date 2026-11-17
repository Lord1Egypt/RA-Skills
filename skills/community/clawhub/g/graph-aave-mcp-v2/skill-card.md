## Description:

Aave V2/V3/V4 MCP server — 62 tools across 18 Graph subgraphs + Aave V4 API + on-chain view contracts. Reserves, positions, cross-chain liquidation risk monitoring with live HF confirmation, governance, V4 hubs/spokes, Base equity gap shock and oracle status, loan-swap analytics, exchange rates, swap quotes, rewards, protocol history, and a durable findings store that survives context compaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulieb14](https://clawhub.ai/user/paulieb14)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this MCP server to query Aave V2/V3/V4 markets, positions, activity, governance, and cross-chain liquidation risk, including live health-factor checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete because one reference could not be resolved; the benign verdict is not a guarantee that the skill is risk-free.

Mitigation: Review the unresolved reference and use the skill only if its Aave query purpose fits your needs.

Risk: Unfiltered Ethereum reserve queries can return about 28k tokens.

Mitigation: Narrow reserve queries with symbols, limit, or compact options.

Risk: Subgraph data can lag behind the chain.

Mitigation: Check the returned freshness metadata, including lagSeconds, when evaluating recency.

## Reference(s):

- [Project homepage](https://github.com/PaulieB14/graph-aave-mcp)
- [npm package](https://www.npmjs.com/package/graph-aave-mcp)
- [The Graph Studio](https://thegraph.com/studio/)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, JSON, Guidance]

**Output Format:** [Structured JSON and text tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reserve queries support symbols, limit, and compact options; freshness metadata may report subgraph lag.]

## Skill Version(s):

4.3.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
