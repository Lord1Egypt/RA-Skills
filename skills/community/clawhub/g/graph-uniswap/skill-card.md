## Description:

Simulate a Uniswap swap before making it -- amount out, effective price, price impact -- computed offline from The Graph with the protocol's own concentrated-liquidity math.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulieb14](https://clawhub.ai/user/paulieb14)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer Uniswap pool, token price, and swap quote questions across supported chains before deciding whether to pursue a trade. It is intended for market data analysis and quote preparation, not trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts an unpinned npm-based MCP server and exposes a Graph API key to that process.

Mitigation: Use a dedicated low-privilege Graph API key, avoid sharing unrelated environment variables with the MCP process, and prefer a pinned or otherwise verified graph-uniswap-mcp version.

Risk: The skill may activate for finance questions that are not specifically about Uniswap.

Mitigation: Confirm the request is about Uniswap before using the skill, and avoid presenting the output as investment advice.

Risk: Swap quotes reflect the most recently indexed subgraph state and do not guarantee execution at inclusion time.

Mitigation: Tell users when results are material, report unquotable reasons instead of substituting estimates, and recommend on-chain quoting for oversized trades or pools with unsupported behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paulieb14/skills/graph-uniswap)
- [The Graph Studio](https://thegraph.com/studio)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or structured text describing Uniswap pools, token prices, recent swaps, and quote results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include amount out, effective price, price impact, fee, ticks crossed, quotability status, and reasons a pool cannot be quoted.]

## Skill Version(s):

0.3.3 (source: release evidence, frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
