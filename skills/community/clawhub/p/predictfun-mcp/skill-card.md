## Description: <br>
Access Predict.fun prediction market data on BNB Chain, including platform stats, market analysis, trader profiling, yield mechanics, and behavioral meta-tools via The Graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PaulieB14](https://clawhub.ai/user/PaulieB14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this MCP server to connect AI agents to Predict.fun market data for market rankings, platform statistics, trader profiling, yield analysis, behavioral scans, and custom GraphQL queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Graph API key usage can consume quota and may expose account usage patterns if shared broadly. <br>
Mitigation: Use a dedicated Graph API key with quota limits and monitor query volume. <br>
Risk: Custom GraphQL queries can increase cost or retrieve broader public market and wallet data than intended. <br>
Mitigation: Review custom queries before use and limit agent access to trusted workflows. <br>
Risk: The optional SSE/HTTP transport can expose the MCP server if bound or proxied to untrusted networks. <br>
Mitigation: Keep the service local by default or place it behind access controls before remote use. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/PaulieB14/predictfun-mcp) <br>
- [Release metadata homepage](https://github.com/PaulieB14/predictfun-subgraphs) <br>
- [Predict.fun](https://predict.fun) <br>
- [The Graph](https://thegraph.com) <br>
- [The Graph API key documentation](https://thegraph.com/docs/en/subgraphs/querying/managing-api-keys/) <br>
- [The Graph GraphQL API documentation](https://thegraph.com/docs/en/querying/graphql-api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [MCP tool responses as Markdown-style text and structured JSON, with setup guidance using shell commands and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and GRAPH_API_KEY; tool calls query The Graph Gateway and optional SSE/HTTP transport can run on a configurable local port.] <br>

## Skill Version(s): <br>
0.5.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
