## Description: <br>
Graph Aave MCP provides an MCP server for querying Aave V2, V3, and V4 market data, positions, liquidation risk, governance, rewards, exchange rates, swap quotes, and protocol history through The Graph, Aave APIs, and on-chain view contracts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulieb14](https://clawhub.ai/user/paulieb14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to inspect Aave markets, user positions, liquidation risk, rewards, governance activity, and V4 hub or spoke data across supported chains. It is intended for data access and analysis, not wallet custody or transaction signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Graph API key and sends Aave-related queries, wallet addresses, and related parameters to The Graph and Aave infrastructure. <br>
Mitigation: Use a separate or least-privilege Graph API key where possible and avoid sharing unnecessary wallet or account data. <br>
Risk: Users may confuse Aave data analysis with wallet custody or transaction execution. <br>
Mitigation: Do not provide wallet private keys or seed phrases; the evidence states the skill does not need them and shows no hidden wallet access or transaction behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paulieb14/graph-aave-mcp-v2) <br>
- [Project homepage](https://github.com/PaulieB14/graph-aave-mcp) <br>
- [npm package](https://www.npmjs.com/package/graph-aave-mcp) <br>
- [The Graph Studio](https://thegraph.com/studio/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API data, configuration, guidance] <br>
**Output Format:** [Markdown or structured MCP tool responses with Aave market, wallet, and protocol data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GRAPH_API_KEY; responses may include wallet addresses, health factors, risk scores, market metrics, rewards, swap quote data, and persisted findings.] <br>

## Skill Version(s): <br>
4.1.21 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
