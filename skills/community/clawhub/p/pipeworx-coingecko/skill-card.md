## Description: <br>
Access real-time cryptocurrency data including coin details, market rankings, trending tokens, and search by name or symbol using CoinGecko's free API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to a Pipeworx-hosted CoinGecko MCP gateway for public cryptocurrency lookup, market ranking, search, and trending-token queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto lookup prompts and queries are sent to an external Pipeworx-hosted CoinGecko MCP gateway. <br>
Mitigation: Use the skill only for public coin and market data, and avoid private portfolio, wallet, exchange-account, or investment-sensitive details unless the gateway operator is trusted. <br>
Risk: Market and trending-token data can be misread as investment advice. <br>
Mitigation: Treat returned data as informational market data and review it against appropriate financial context before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-coingecko) <br>
- [Pipeworx CoinGecko MCP gateway](https://gateway.pipeworx.io/coingecko/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets and MCP tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only public cryptocurrency data responses through an external MCP gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
