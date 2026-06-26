## Description: <br>
Harena connects AI assistants to Harena's MCP service for 24/7 market monitoring, personalized news analysis, trading signals, and alerts across crypto and US stocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wall-e](https://clawhub.ai/user/wall-e) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Harena to ask an AI assistant for market briefings, symbol analysis, alerts, watchlist and topic management, and profile personalization through Harena's MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market interests, watchlists, topic subscriptions, profile preferences, and API-key-authenticated requests are sent to Harena's MCP service. <br>
Mitigation: Install only if you trust Harena and are comfortable sharing that information with the service. <br>
Risk: The skill can register accounts and change profile, watchlist, and topic-subscription settings through MCP tools. <br>
Mitigation: Confirm the user's intent before registration or before changing profile, watchlist, or subscription settings. <br>
Risk: HARENA_API_KEY values and API keys returned during registration are sensitive secrets. <br>
Mitigation: Store API keys in environment variables or client secret storage and avoid exposing them in shared logs, prompts, or screenshots. <br>
Risk: Financial-market analysis, alerts, and trading signals can be incomplete, delayed, or wrong. <br>
Mitigation: Treat outputs as informational and verify important market information independently before making trading decisions. <br>


## Reference(s): <br>
- [Harena homepage](https://harena.world) <br>
- [Harena install guide](https://www.harena.world/install) <br>
- [Harena MCP docs](https://www.harena.world/mcp/docs) <br>
- [Harena MCP discovery](https://www.harena.world/.well-known/mcp.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Natural-language responses, MCP tool results, JSON examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated tools require HARENA_API_KEY; registration tools can return a new API key.] <br>

## Skill Version(s): <br>
0.3.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
