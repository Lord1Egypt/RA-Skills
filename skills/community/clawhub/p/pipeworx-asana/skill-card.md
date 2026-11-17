## Description:

Pipeworx Asana lets an agent access Asana workspaces, projects, and tasks through an OAuth-backed MCP server for listing, searching, retrieving task details, and creating tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to connect to Asana through Pipeworx, inspect accessible workspaces and projects, search or read task information, and create project tasks from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth-backed Asana access is routed through an unverified third-party MCP gateway with write capability.

Mitigation: Review who operates gateway.pipeworx.io and what OAuth scopes it requests before authorizing it.

Risk: The skill can create tasks and expose task metadata from connected Asana workspaces.

Mitigation: Use the least-privileged Asana workspace and project access available, and avoid connecting sensitive workspaces unless the third-party gateway is acceptable for the data involved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-asana)
- [Configured Pipeworx Asana MCP endpoint](https://gateway.pipeworx.io/asana/mcp)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Markdown with JSON MCP server configuration and concise tool-use descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return Asana workspace, project, task, assignee, due date, completion status, permalink, and search result details through the configured MCP server.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
