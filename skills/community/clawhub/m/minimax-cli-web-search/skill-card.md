## Description: <br>
MiniMax CLI Web Search runs web search through MiniMax MCP with a local mcporter wrapper, preflight checks, API-key/config checks, and normalized result formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biggersun](https://clawhub.ai/user/biggersun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill when they need current web search results, source links, quick research, or time-sensitive facts through a configured MiniMax MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the configured MiniMax MCP provider and may expose sensitive prompt content. <br>
Mitigation: Do not include passwords, API keys, confidential documents, or sensitive business details in search queries. <br>
Risk: The skill depends on the local mcporter installation and MiniMax MCP configuration. <br>
Mitigation: Run the documented preflight check before use and install only when the local mcporter setup and MiniMax MCP configuration are trusted. <br>
Risk: Network, timeout, or upstream response variance can produce failed or low-quality searches. <br>
Mitigation: Use the normalized JSON mode for automation, adjust the timeout when needed, and retry with narrower queries or counts. <br>


## Reference(s): <br>
- [Environment Checklist](references/environment-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus plain-text or normalized JSON search results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include top-N titles, URLs, snippets, and dates when available; raw MiniMax MCP JSON can also be returned.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
