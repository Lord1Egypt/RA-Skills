## Description:

NexusTrader trading assistant. Query crypto balances, positions, prices, and place orders on Binance, Bybit, OKX, Bitget, HyperLiquid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quantweb3-scott](https://clawhub.ai/user/quantweb3-scott)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use NexusTrader to query crypto balances, positions, prices, klines, and open orders, and to route order-management requests through a local MCP server for supported exchanges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use local exchange API keys and may have live trading authority.

Mitigation: Use testnet or demo keys first, remove withdrawal permissions, and avoid live accounts until order-changing tools have code-level confirmation or allowlist controls.

Risk: Order-changing safeguards are mostly instructional.

Mitigation: Require explicit user confirmation before create, cancel, or modify order calls and review the agent flow before enabling live trading.

Risk: An enabled background daemon can hold access to exchange API keys.

Mitigation: Keep auto-start disabled unless intentionally needed, and restrict the MCP server to a trusted local endpoint.

Risk: Installation guidance includes curl-to-shell style commands.

Mitigation: Review install commands and scripts before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quantweb3-scott/skills/nexustrader)
- [ClawHub publisher profile](https://clawhub.ai/user/quantweb3-scott)
- [Referenced NexusTrader-mcp documentation](https://github.com/Quantweb3-com/NexusTrader-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, raw JSON from bridge commands, shell command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include account and market data from a local MCP server; order-changing actions require explicit user confirmation.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
