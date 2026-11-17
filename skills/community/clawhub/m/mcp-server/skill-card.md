## Description:

Create and deploy Model Context Protocol (MCP) servers for AI agents. MCP enables AI models to interact with external tools and services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinakingkong](https://clawhub.ai/user/chinakingkong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create MCP server templates, connect AI agents to external APIs and services, and prepare deployments for agent integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated MCP servers may access external APIs, databases, filesystems, or command execution.

Mitigation: Review generated server code before use, scope credentials and filesystem or database access, and require explicit confirmation for deployments, writes, file management, and command execution.

Risk: Agent integrations may connect deployed servers to privileged external services.

Mitigation: Use least-privilege API keys and confirm deployment settings before connecting the MCP server to an agent.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated server templates, deployment commands, and configuration steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
