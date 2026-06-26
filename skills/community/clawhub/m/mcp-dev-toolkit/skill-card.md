## Description: <br>
Build, test, and deploy MCP (Model Context Protocol) tools for developer workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold Python or TypeScript MCP servers, define tools, choose transports, and apply database, file, and API integration patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated MCP servers may expose broad file, API, or database access if deployed without scoping. <br>
Mitigation: Review generated tools before deployment, restrict file paths and API domains, and use least-privilege database credentials. <br>
Risk: Dependency choices in scaffolded Python or TypeScript servers may drift over time. <br>
Mitigation: Use lockfiles or pinned dependency review before installing or deploying scaffolded servers. <br>


## Reference(s): <br>
- [Database MCP Tool Patterns](references/database-tools.md) <br>
- [File Management MCP Tool Patterns](references/file-tools.md) <br>
- [API Integration MCP Tool Patterns](references/api-tools.md) <br>
- [ClawHub skill page](https://clawhub.ai/evezart/mcp-dev-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/evezart) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scaffolded MCP server files when the included scaffold script is executed by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
