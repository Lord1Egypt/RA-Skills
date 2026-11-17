## Description:

MCP server for the PracticePanther legal practice management API that exposes PracticePanther's REST API as read-only MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjquinlan2000](https://clawhub.ai/user/mjquinlan2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and legal operations teams use this skill to let an agent inspect PracticePanther legal practice management data through read-only MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects an agent to PracticePanther account data through an external MCP package.

Mitigation: Install only after trusting the external package, verify the exposed MCP tools before use, and connect only data the agent is permitted to inspect.

Risk: The MCP server requires an API credential that can expose sensitive legal practice information.

Mitigation: Use the least-privileged available credential and avoid connecting client or matter data outside the intended agent scope.

## Reference(s):

- [PracticePanther MCP npm package](https://www.npmjs.com/package/@mjquinlan2000/practicepanther-mcp)
- [ClawHub skill page](https://clawhub.ai/mjquinlan2000/skills/practicepanther-mcp)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and MCP tool call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter, practicepanther-mcp, and NODE_MCP_SECRET_KEY.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
