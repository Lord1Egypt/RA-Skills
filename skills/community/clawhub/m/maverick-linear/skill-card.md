## Description: <br>
Read and write Linear workspace data via Linear's hosted MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to let an agent inspect Linear work and perform confirmed Linear updates through Linear's hosted MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can create, update, or delete Linear records visible to the connected workspace. <br>
Mitigation: Confirm specific user intent before write, create, or delete calls, and avoid broad batch changes unless the user explicitly approves the batch. <br>
Risk: The setup flow stores Linear OAuth credentials locally and can overwrite existing vault values during credential rotation. <br>
Mitigation: Run setup only with fresh OAuth values, rotate credentials intentionally, and revoke the Linear grant when access is no longer needed. <br>
Risk: Tool arguments and results are sent to Linear's hosted MCP server. <br>
Mitigation: Send only Linear-relevant content and avoid passing unrelated secrets, credentials, or unnecessary personal data through tool arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick/maverick-linear) <br>
- [Maverick publisher profile](https://clawhub.ai/user/maverick) <br>
- [Linear MCP documentation](https://linear.app/docs/mcp) <br>
- [Linear hosted MCP endpoint](https://mcp.linear.app/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON or text returned by mcporter tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter and Linear OAuth credentials; live tool schemas are discovered from Linear's hosted MCP server.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
