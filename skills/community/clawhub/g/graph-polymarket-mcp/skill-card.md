## Description: <br>
Query Polymarket prediction market data via The Graph subgraphs and Polymarket REST APIs for market search, live prices, on-chain analytics, trader P&L, open interest, resolution status, and related analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulieb14](https://clawhub.ai/user/paulieb14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this MCP server to search Polymarket markets, retrieve live CLOB prices and order books, and query The Graph subgraphs for on-chain analytics, trader performance, open interest, and resolution data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Graph API key could be exposed or overused. <br>
Mitigation: Use a dedicated Graph API key, keep it in environment configuration, and monitor quota. <br>
Risk: The optional HTTP/SSE endpoint could be reachable by untrusted clients. <br>
Mitigation: Prefer local stdio use; when HTTP/SSE is required, restrict network exposure and add firewalling, authentication, and TLS through a trusted proxy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/paulieb14/graph-polymarket-mcp) <br>
- [Project Homepage](https://github.com/PaulieB14/graph-polymarket-mcp) <br>
- [The Graph Studio](https://thegraph.com/studio/) <br>
- [Polymarket](https://polymarket.com/) <br>
- [npm Package](https://www.npmjs.com/package/graph-polymarket-mcp) <br>
- [MCP Registry Entry](https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.PaulieB14/graph-polymarket-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Configuration] <br>
**Output Format:** [MCP tool responses containing JSON-formatted text plus configuration guidance for stdio or SSE transport.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Subgraph tools require GRAPH_API_KEY; REST API tools use public Polymarket endpoints without authentication.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
