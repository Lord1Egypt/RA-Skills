## Description:

Provides cryptocurrency trading data analytics including smart money tracking, whale monitoring, market data queries, and trader statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[develophyperbotnetwork](https://clawhub.ai/user/develophyperbotnetwork)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to connect an MCP-capable client to Hyperbot trading analytics for market data, smart-money discovery, whale monitoring, and trader performance analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses, coin interests, and trading-analysis queries are sent to external Hyperbot and related market-data services.

Mitigation: Use the skill only when that data sharing is acceptable, and avoid entering seed phrases, private keys, exchange credentials, authorization tokens, or other secrets.

Risk: The installation guidance includes unpinned npm bridge installs for MCP connectivity.

Mitigation: Prefer pinned and reviewed MCP bridge dependencies in an isolated environment before enabling the remote server.

Risk: Trading analytics can be incomplete, delayed, or unsuitable as the sole basis for financial decisions.

Mitigation: Review outputs as informational analysis, cross-check important conclusions, and apply independent risk controls before acting.

## Reference(s):

- [Hyperbot MCP Prompts Reference](references/prompts-reference.md)
- [Hyperbot MCP SSE endpoint](https://mcp.hyperbot.network/mcp/sse)
- [Hyperbot MCP message endpoint](https://mcp.hyperbot.network/mcp/message)
- [ClawHub skill page](https://clawhub.ai/develophyperbotnetwork/skills/hyperbot-quote-mcp)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON, JSON-RPC, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only trading analytics guidance from Hyperbot MCP tool responses; outputs may include market summaries, trader evaluations, whale activity analysis, and MCP client configuration snippets.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
