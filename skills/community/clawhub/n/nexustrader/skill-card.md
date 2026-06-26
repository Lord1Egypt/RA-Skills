## Description: <br>
NexusTrader trading assistant. Query crypto balances, positions, prices, and place orders on Binance, Bybit, OKX, Bitget, HyperLiquid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quantweb3-scott](https://clawhub.ai/user/quantweb3-scott) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to a local NexusTrader MCP server for crypto account queries, market data lookups, position review, and user-confirmed order management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place, cancel, or modify real crypto orders when configured with exchange credentials. <br>
Mitigation: Use testnet or read-only/scoped keys first, and require explicit user confirmation before every order-management action. <br>
Risk: If auto-start is enabled, a background NexusTrader MCP daemon can run with access to local exchange API keys. <br>
Mitigation: Keep auto-start disabled unless needed, start and stop the server manually, and review daemon status and logs before live use. <br>
Risk: Installer or setup commands may execute remote tooling and configure local trading access. <br>
Mitigation: Inspect installer commands before running them and verify that credentials remain in the local .keys/.secrets.toml file. <br>


## Reference(s): <br>
- [NexusTrader ClawHub release](https://clawhub.ai/quantweb3-scott/nexustrader) <br>
- [Publisher profile](https://clawhub.ai/user/quantweb3-scott) <br>
- [NexusTrader-mcp upstream documentation](https://github.com/Quantweb3-com/NexusTrader-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and formatted trading data from local MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return JSON-derived balances, positions, prices, open orders, status, and order-management results.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
