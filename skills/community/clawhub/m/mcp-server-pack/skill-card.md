## Description:

MCP Server Pack provides managed MCP servers for filesystem, memory, GitHub, Postgres, web search, and RSS access, with OpenClaw configuration for cloud-hosted or self-hosted use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neroagent](https://clawhub.ai/user/neroagent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to discover available MCP servers and generate OpenClaw MCP client configuration for cloud-hosted, self-hosted, or hybrid setups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated configurations can run unpinned Docker images or npm packages with local file access.

Mitigation: Pin Docker images by digest and npm packages by exact version, and mount only narrow directories as read-only unless writes are required.

Risk: GitHub and PostgreSQL integrations may require credentials or connection strings.

Mitigation: Use short-lived, fine-grained credentials and keep secrets out of reusable configuration examples.

Risk: Cloud-hosted MCP servers may receive user data from configured tools or mounted sources.

Mitigation: Confirm what data is sent to the hosted service before use and avoid routing sensitive data unless approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neroagent/skills/mcp-server-pack)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands, guidance]

**Output Format:** [Text and JSON configuration with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Docker, npx, environment variables, MCP connection details, and cloud or self-hosted setup guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
