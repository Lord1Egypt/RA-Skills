## Description: <br>
MCP server for the Lawmatics legal CRM API. Exposes Lawmatics' REST API as read-only MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjquinlan2000](https://clawhub.ai/user/mjquinlan2000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this MCP server to list and call read-only tools for the Lawmatics legal CRM API through mcporter over stdio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced npm package is third-party software outside the submitted artifact. <br>
Mitigation: Confirm trust in the npm package before installing or running the MCP server. <br>
Risk: Lawmatics CRM records may include sensitive client or matter data. <br>
Mitigation: Use a Lawmatics API key with the narrowest available read-only permissions and inspect available tools with mcporter before calling them. <br>


## Reference(s): <br>
- [Lawmatics MCP npm package](https://www.npmjs.com/package/@mjquinlan2000/lawmatics-mcp) <br>
- [Lawmatics API MCP ClawHub release](https://clawhub.ai/mjquinlan2000/lawmatics-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance, API calls] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only MCP tools require mcporter, lawmatics-mcp, and NODE_MCP_SECRET_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
