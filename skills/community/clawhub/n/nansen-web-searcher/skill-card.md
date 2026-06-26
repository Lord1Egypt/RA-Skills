## Description: <br>
Search the web for one or more queries in parallel. Use when you need current information, news, prices, or any web content to complement on-chain Nansen data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Nansen web searches for current information, market news, prices, and web context that can complement on-chain analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires the nansen CLI and access to NANSEN_API_KEY. <br>
Mitigation: Install only if you trust the nansen-cli package, scope API key access appropriately, and keep use focused on web search and fetch commands. <br>
Risk: Search queries may expose secrets or private business information to external services. <br>
Mitigation: Avoid putting secrets, credentials, or sensitive private information into search queries. <br>


## Reference(s): <br>
- [Nansen Web Searcher on ClawHub](https://clawhub.ai/nansen-devops/nansen-web-searcher) <br>
- [nansen-devops publisher profile](https://clawhub.ai/user/nansen-devops) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include one entry per query with organic results and optional knowledge graph data; results per query are configurable from 1 to 20.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
