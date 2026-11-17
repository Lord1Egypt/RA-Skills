## Description:

IPInfo MCP wraps ipinfo.io for basic IP lookups without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can connect an MCP server that provides IP address lookup and current-client-IP lookup tools backed by ipinfo.io.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses a mutable npm package with automatic confirmation.

Mitigation: Use a pinned, audited mcp-remote version or a lockfile-based setup before installation.

Risk: IP lookups are sent through a third-party gateway.

Mitigation: Only submit IP addresses that are acceptable to share with the external service.

Risk: Lookup results are external data.

Mitigation: Treat returned data as untrusted context and review it before using it in decisions or instructions.

## Reference(s):

- [Pipeworx ipinfo pack](https://pipeworx.io/packs/ipinfo)
- [Pipeworx](https://pipeworx.io)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-ipinfo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown with JSON configuration snippets and tool-use guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces IP lookup results through an external MCP gateway; results should be treated as external data.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
