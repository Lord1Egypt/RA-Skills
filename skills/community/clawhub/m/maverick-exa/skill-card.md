## Description:

Exa MCP helps agents run Exa web and people research, select the fixed hosted MCP tools, troubleshoot rate limits, and return concise source-linked summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to configure hosted Exa MCP access and run broad, advanced, or people-focused web research with source-linked results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted MCP URL places the Exa API key in a query string, which can expose the key if copied into logs, diagnostics, or shared configuration files.

Mitigation: Use a dedicated limited Exa API key, keep MCP configuration and logs private, and rotate the key if the expanded endpoint URL may have been shared.

Risk: Broad web or people searches can return incomplete, noisy, or outdated findings.

Mitigation: Prefer constrained advanced searches for precision work and return source links with explicit unknowns.

## Reference(s):

- [Exa MCP Setup](references/exa-mcp-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with links, inline tool names, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source links, explicit unknowns, MCP endpoint guidance, and rate-limit troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
