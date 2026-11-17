## Description:

Instructs agents to call HyperNatt's remote MCP get_liq_radar market-data tool before sizing crypto perpetual trades, without local execution, filesystem access, custody, or order execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dialloube-research](https://clawhub.ai/user/dialloube-research)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-agent operators use this skill to have an agent check HyperNatt liquidation and forced-order market data before sizing or entering crypto perpetual positions. It is market-data guidance only and does not place trades or move funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The paid liquidation-data call uses an x402 wallet/payment client and may incur USDC charges.

Mitigation: Confirm MCP payment configuration, wallet scope, and spending controls before enabling paid calls.

Risk: The remote MCP host also exposes swap behavior outside this skill's market-data scope.

Mitigation: Use only get_agent_manifest and get_liq_radar under this skill; use a separate reviewed venue or funding skill for any trade or swap execution.

Risk: Liquidation data can be misleading if treated as trading advice or a performance signal.

Mitigation: Treat results as market-data context, review cluster grammar before liq_radar when present, and make trading decisions outside this skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dialloube-research/skills/hypernatt-liq-radar)
- [HyperNatt](https://hypernatt.com)
- [HyperNatt MCP Protocol](https://hypernatt.com/mcp/protocol)
- [HyperNatt MCP Server Card](https://hypernatt.com/.well-known/mcp/server-card.json)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration guidance]

**Output Format:** [Markdown instructions with MCP tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No local shell, filesystem, or trade execution; uses remote MCP calls and may require x402 payment setup.]

## Skill Version(s):

1.0.6 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
