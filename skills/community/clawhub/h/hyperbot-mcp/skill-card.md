## Description: <br>
Provides cryptocurrency trading analytics through Hyperbot's remote MCP service, including smart money tracking, whale monitoring, market data queries, and trader performance statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[developHyperbotNetwork](https://clawhub.ai/user/developHyperbotNetwork) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and AI agents use this skill to query Hyperbot trading data, analyze wallet and whale behavior, evaluate trader performance, and generate cryptocurrency market research. Outputs should support research workflows and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, address batches, session IDs, and trading-analysis queries are sent to Hyperbot's remote service. <br>
Mitigation: Avoid submitting sensitive client, proprietary, or regulated address lists unless the provider's data handling is trusted. <br>
Risk: Strategy suggestions, trader scores, and market predictions may be wrong or unsuitable for financial decisions. <br>
Mitigation: Treat outputs as informational research and require independent review before trading or investment use. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/developHyperbotNetwork/hyperbot-mcp) <br>
- [Hyperbot MCP endpoint](https://mcp.hyperbot.network/mcp) <br>
- [Hyperbot MCP SSE endpoint](https://mcp.hyperbot.network/mcp/sse) <br>
- [Prompts reference](references/prompts-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON-formatted analysis with MCP JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trading analytics, wallet statistics, market data summaries, strategy suggestions, and API call examples.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
