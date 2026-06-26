## Description: <br>
Provides cryptocurrency trading data analytics including smart money tracking, whale monitoring, market data queries, and trader statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[developHyperbotNetwork](https://clawhub.ai/user/developHyperbotNetwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to connect agents to Hyperbot's remote MCP server for cryptocurrency market data, whale monitoring, smart money discovery, and trader performance analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects agents to a third-party remote MCP endpoint and may require npm connector packages for some clients. <br>
Mitigation: Install it only when the user trusts Hyperbot, the remote MCP endpoint, and any connector package required by the chosen MCP client. <br>
Risk: Wallet addresses submitted to the MCP server may reveal trading or portfolio interests. <br>
Mitigation: Avoid submitting wallet addresses the user considers sensitive and disclose that address-based queries are sent to the remote Hyperbot service. <br>
Risk: Crypto market analysis and trading recommendations can be incorrect, stale, or unsuitable for real trades. <br>
Mitigation: Treat outputs as informational analysis, verify data independently, and do not use the skill as the sole basis for trading decisions. <br>


## Reference(s): <br>
- [Hyperbot MCP Prompts Reference](references/prompts-reference.md) <br>
- [Hyperbot MCP SSE Endpoint](https://mcp.hyperbot.network/mcp/sse) <br>
- [Hyperbot MCP Message Endpoint](https://mcp.hyperbot.network/mcp/message) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON-RPC examples, configuration snippets, and analytical text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include cryptocurrency market analysis, wallet-address based trader summaries, and informational trading recommendations.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
