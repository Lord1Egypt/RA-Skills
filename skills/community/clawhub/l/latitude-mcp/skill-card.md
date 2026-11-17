## Description:

Connect OpenClaw to the Latitude MCP server so the agent can read and manage Latitude workspace resources such as projects, traces, spans, issues, annotations, scores, saved searches, datasets, monitors, and members.

This skill is ready for commercial/non-commercial use.

## Publisher:

[latitude](https://clawhub.ai/user/latitude)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using Latitude use this skill to add Latitude as an OAuth-authenticated remote MCP server in OpenClaw. It helps agents query and manage observability and evaluation resources in an authorized Latitude workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth-backed access may allow an agent to read or manage sensitive Latitude workspace resources.

Mitigation: Use the least-privileged Latitude account or organization available, inspect exposed tools with the probe command, add a toolFilter for routine use, and revoke or logout when access is no longer needed.

## Reference(s):

- [Latitude MCP documentation](https://docs.latitude.so/getting-started/mcp)
- [Latitude](https://latitude.so)
- [Model Context Protocol](https://modelcontextprotocol.io)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OAuth setup, connection probing, logout, self-hosted URL, and tool filtering guidance.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
