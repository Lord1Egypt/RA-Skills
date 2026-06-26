## Description: <br>
Query Limitless prediction markets on Base - live odds, trader P&L, whale tracking, market stats, and daily volume from The Graph's decentralized network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulieb14](https://clawhub.ai/user/paulieb14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Limitless prediction market activity on Base, including market stats, trades, trader analytics, positions, leaderboards, and whale activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs through an external npm package. <br>
Mitigation: Install only if the package source is trusted and review updates before deployment. <br>
Risk: Limitless-related prompts may send market queries and the GRAPH_API_KEY to external endpoints. <br>
Mitigation: Use a dedicated revocable GRAPH_API_KEY and avoid including private information in prompts that could trigger market lookups. <br>
Risk: The skill may be invoked autonomously for Limitless prediction market questions. <br>
Mitigation: Disable the skill when automatic Limitless lookups are not desired. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/paulieb14/graph-limitless-mcp) <br>
- [npm package](https://www.npmjs.com/package/graph-limitless-mcp) <br>
- [The Graph API keys](https://thegraph.market/dashboard#api-keys) <br>
- [Limitless](https://limitless.exchange) <br>
- [The Graph](https://thegraph.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Natural-language and Markdown market data summaries; setup guidance may include shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and GRAPH_API_KEY; queries are sent to The Graph Gateway and the Limitless API, with no persistent local storage disclosed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
