## Description: <br>
MCP server for the PracticePanther legal practice management API that exposes PracticePanther's REST API as read-only MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjquinlan2000](https://clawhub.ai/user/mjquinlan2000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers configuring agent access to PracticePanther use this skill to connect an MCP client to read-only tools for the PracticePanther REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external MCP connector can expose sensitive PracticePanther legal-practice data to an agent. <br>
Mitigation: Use the least-privileged read-only credential available, verify the practicepanther-mcp package and maintainer, and inspect the listed MCP tools before calling them. <br>
Risk: PracticePanther credentials must be provided for the MCP connector to run. <br>
Mitigation: Provide NODE_MCP_SECRET_KEY through a controlled environment or secret manager and confirm how credentials are stored before deployment. <br>


## Reference(s): <br>
- [PracticePanther API MCP on ClawHub](https://clawhub.ai/mjquinlan2000/practicepanther-mcp) <br>
- [practicepanther-mcp npm package](https://www.npmjs.com/package/@mjquinlan2000/practicepanther-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter, practicepanther-mcp, and NODE_MCP_SECRET_KEY; configured MCP tool calls should remain read-only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
