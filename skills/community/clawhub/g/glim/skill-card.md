## Description: <br>
glim.sh connects agents to Glim's hosted MCP server for live Twitter/X, Reddit, web, GitHub, Amazon, and YouTube data, using OAuth prepaid billing or pay-per-call crypto payments without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect MCP-capable agents to paid live-data tools for social search, web search and extraction, GitHub lookups, Amazon product data, and YouTube transcripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tool calls are sent to an external paid provider and may include search queries, fetched URLs, and related tool-call metadata. <br>
Mitigation: Avoid secrets, private company URLs, personal data, and sensitive research unless the provider's privacy and billing terms are approved; restrict enabled tools with the documented tools parameter and use scoped MCP configuration where supported. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/glim) <br>
- [glim.sh](https://glim.sh) <br>
- [Glim OpenAPI specification](https://glim.sh/openapi.json) <br>
- [Glim GitHub resources](https://github.com/glim-sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide configuration of an external hosted MCP service and paid tool calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
