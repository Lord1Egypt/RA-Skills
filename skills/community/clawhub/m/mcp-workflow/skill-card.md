## Description: <br>
Workflow automation using MCP (Model Context Protocol) patterns inspired by Jason Zhou. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slemo54](https://clawhub.ai/user/slemo54) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to create and run MCP-style workflows with prompt chains, resource templates, workflow templates, and local MCP server tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server can read local files available to its process. <br>
Mitigation: Run it only with trusted clients, preferably inside a restricted project directory or sandbox. <br>
Risk: Persistent workflow memory or logs may retain sensitive data. <br>
Mitigation: Avoid storing secrets in workflow memory or logs, and add redaction and retention practices before wider deployment. <br>


## Reference(s): <br>
- [MCP Workflow skill page](https://clawhub.ai/slemo54/mcp-workflow) <br>
- [MCP Specification](references/mcp-spec.md) <br>
- [Workflow Patterns](references/workflow-patterns.md) <br>
- [Jason Zhou Insights](references/jason-zhou-insights.md) <br>
- [MCP Official Site](https://modelcontextprotocol.io/) <br>
- [MCP SDK Documentation](https://github.com/modelcontextprotocol/sdk) <br>
- [MCP Example Servers](https://github.com/modelcontextprotocol/servers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON workflow templates, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP server operations, workflow template usage, validation commands, and workflow design guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
