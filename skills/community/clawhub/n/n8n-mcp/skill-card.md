## Description: <br>
Connects agents to an n8n MCP server to create, update, test, execute, and manage workflows, data tables, projects, folders, and SDK-built workflow code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itian932](https://clawhub.ai/user/itian932) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to administer n8n through MCP, including workflow creation, workflow testing and execution, node discovery, project and folder lookup, and data-table management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer an n8n instance and make real workflow or data-table changes. <br>
Mitigation: Use a least-privilege token, review generated workflows before creation, test before publishing, and require explicit confirmation before production execution, publishing, archiving, deleting columns, or bulk data-table changes. <br>
Risk: The skill requires an MCP endpoint and sensitive bearer token. <br>
Mitigation: Keep the MCP endpoint protected and store N8N_MCP_TOKEN only in the agent runtime's secret or environment management system. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/itian932/n8n-mcp) <br>
- [n8n service endpoint from metadata](http://localhost:5678) <br>
- [n8n MCP endpoint from skill configuration](http://localhost:5678/mcp-server/http) <br>
- [Common n8n Nodes Reference](references/common-nodes.md) <br>
- [n8n Workflow SDK Patterns](references/sdk-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, TypeScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call MCP tools that change n8n workflows and data tables when configured with N8N_MCP_URL and N8N_MCP_TOKEN.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
