## Description:

Jikan MCP wraps the Jikan v4 API for free, no-auth anime and manga data lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect to a Pipeworx-hosted Jikan MCP server for anime, manga, and character lookups without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connection instructions run mutable third-party code on the user's machine through mcp-remote.

Mitigation: Review the connection command before installation, prefer a pinned mcp-remote version or managed lockfile, and run the MCP server with only the local and network access needed for Jikan lookups.

## Reference(s):

- [Pipeworx Jikan Pack](https://pipeworx.io/packs/jikan)
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-jikan)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with JSON configuration and inline command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs MCP connection guidance for using the remote Jikan service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
