## Description: <br>
Use the MCPHero Meta-MCP server inside AI clients such as Claude Desktop and Cursor to create, deploy, and manage MCP servers through the wizard pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arterialist](https://clawhub.ai/user/arterialist) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect an MCP-compatible client to MCPHero's Meta-MCP service, walk through the hosted wizard flow, and configure deployed MCP servers for reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects an AI client to a persistent hosted MCP service that may receive prompts, requirements, generated tool definitions, and deployment credentials. <br>
Mitigation: Use the skill only with trusted MCPHero accounts and data, and avoid sending sensitive production requirements unless that use is approved. <br>
Risk: Generated server configurations may include Authorization headers or bearer tokens. <br>
Mitigation: Use least-privilege or short-lived secrets, protect MCP client config files, and rotate exposed tokens. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/arterialist/meta-mcp-creator) <br>
- [MCPHero](https://mcphero.app) <br>
- [Meta-MCP endpoint](https://api.mcphero.app/mcp/meta/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets and tool-call sequencing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP client configuration examples, polling guidance, and credential-handling reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
