## Description: <br>
Maverick Exa guides agents through Exa MCP web discovery, advanced constrained search, people lookup, hosted MCP setup, rate-limit troubleshooting, and concise source-linked research summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure Exa's hosted MCP server and choose the appropriate enabled Exa search tool for web, advanced, or people research. It is intended for concise, source-linked research findings and MCP setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hosted MCP URL uses an Exa API key, which can be exposed if the expanded URL is hardcoded, logged, or shared. <br>
Mitigation: Use a revocable Exa API key from an environment variable and avoid sharing the expanded MCP URL. <br>
Risk: Research queries and people lookups are sent to Exa. <br>
Mitigation: Avoid confidential research topics or people lookups unless Exa's data handling fits the deployment requirements. <br>


## Reference(s): <br>
- [Exa MCP Setup](references/exa-mcp-setup.md) <br>
- [Maverick Exa on ClawHub](https://clawhub.ai/maverick/maverick-exa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Concise Markdown with links and JSON MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a fixed Exa MCP tool set: web_search_exa, web_search_advanced_exa, and people_search_exa.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
