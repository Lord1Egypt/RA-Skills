## Description:

Manage Asana tasks, projects, portfolios, goals, and team workspaces through Asana's hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

Asana users and teams use the skill to find and manage tasks, projects, portfolios, goals, assignees, and workspaces through natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changes can affect shared Asana workspace data.

Mitigation: Require explicit user intent for each write operation and verify the target task, project, portfolio, goal, or workspace object before changing it.

Risk: The OAuth grant provides access under the connected Asana account, and stored credentials could be exposed.

Mitigation: Protect the OAuth credentials, run setup only with fresh credentials, and revoke access in Asana when it is no longer needed.

## Reference(s):

- [Asana MCP Server](https://developers.asana.com/docs/mcp-server)
- [Integrating with Asana's MCP Server](https://developers.asana.com/docs/integrating-with-asanas-mcp-server)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Natural-language responses and structured results from Asana MCP tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The live Asana MCP server determines the available tools; workspace changes require explicit user intent.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
