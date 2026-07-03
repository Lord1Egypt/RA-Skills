## Description: <br>
一个通过Model Context Protocol提供HackerNews内容搜索、检索和分析的服务，适用于AI代理和开发者。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI agents and developers use this skill to search Hacker News content, inspect front-page or recent posts, retrieve item details, and look up public user profiles through the configured API service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes Hacker News queries and the configured API key to an unrelated xiaobenyang.com backend. <br>
Mitigation: Install only if the user trusts xiaobenyang.com with those queries and credentials. <br>
Risk: The skill can persist the API key locally in a .env file as XBY_APIKEY. <br>
Mitigation: Review or remove the .env file when the skill should no longer retain API access. <br>
Risk: Server security evidence marks the release suspicious because of backend routing and disclosure mismatches. <br>
Mitigation: Review the skill and its security evidence before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/hackernews-search) <br>
- [Publisher profile](https://clawhub.ai/user/cainingnk) <br>
- [XiaoBenYang API key service](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP backend](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, API calls, configuration guidance] <br>
**Output Format:** [Markdown summaries derived from JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY value and returns raw API data for the agent to summarize.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
