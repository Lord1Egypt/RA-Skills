## Description:

Connects agents to Aave V2, V3, and V4 data for cross-chain market analysis, position monitoring, and read-only risk and swap-quote queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulieb14](https://clawhub.ai/user/paulieb14)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the MCP server to query Aave markets and positions across supported chains, monitor liquidation risk, and inspect V4 activity. Risk-sensitive decisions can use its live on-chain position checks alongside subgraph data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security analysis was partial because a local reference could not be resolved; the benign verdict has medium confidence.

Mitigation: Review the unresolved reference and treat the security analysis as incomplete when deciding whether to install.

Risk: Subgraph data and prices can lag, which may affect time-sensitive position or market assessments.

Mitigation: Check freshness indicators and confirm critical position health factors with the live on-chain tools.

## Reference(s):

- [ClawHub release](https://clawhub.ai/paulieb14/skills/graph-aave-mcp-v2)
- [Project homepage](https://github.com/PaulieB14/graph-aave-mcp)
- [npm package](https://www.npmjs.com/package/graph-aave-mcp)
- [The Graph API key setup](https://thegraph.com/studio/)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Text]

**Output Format:** [Structured JSON data with textual summaries and analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include subgraph freshness indicators; live RPC-backed tools can confirm position health factors on chain.]

## Skill Version(s):

4.3.4 (source: artifact frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
