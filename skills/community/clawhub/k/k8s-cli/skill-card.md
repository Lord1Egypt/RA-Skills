## Description:

kubectl-mcp-server CLI commands for tool discovery, direct invocation, and diagnostics. Use when exploring available tools, calling tools from command line, or checking server health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to discover kubectl-mcp-server tools, check server and cluster health, and invoke Kubernetes operations from the command line. It also provides examples for configuring local or remote MCP access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote-server example omits protections that restrict access to cluster-management capabilities.

Mitigation: Prefer local stdio access. Before enabling remote HTTP access, configure authentication and network restrictions; use least-privilege Kubernetes credentials, verify read-only mode for the installed version, and confirm the cluster and namespace before changes.

## Reference(s):

- [ClawHub release](https://clawhub.ai/rohitg00/skills/k8s-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples include kubectl-mcp-server commands, JSON arguments, and MCP server configuration.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
