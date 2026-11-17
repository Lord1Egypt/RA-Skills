## Description:

Configures and manages MCP servers so an AI agent can call external tools such as visual understanding and web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godzff](https://clawhub.ai/user/godzff)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to install mcporter, create MCP server configuration, validate server health, and call MCP tools for tasks such as image understanding and web search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance includes unpinned package commands and a remote installer command.

Mitigation: Pin package versions where possible, verify package provenance before installation, and avoid curl-to-shell installers in managed environments.

Risk: The MCP configuration handles API keys and can route prompts, images, or other user data through configured tools.

Mitigation: Store API keys with restrictive permissions or environment-managed secrets, and avoid sending sensitive data unless the MCP provider and package chain are trusted.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/godzff/skills/mcp-protocol)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP server configuration examples, validation commands, tool-call examples, a package list, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
