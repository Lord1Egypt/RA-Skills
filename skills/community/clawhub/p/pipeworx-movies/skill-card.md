## Description:

Movies MCP wraps the iTunes Search API for movie search and the TVmaze API for TV show search, show details, and schedules without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect an MCP server that searches movies, searches TV shows, retrieves TV show details, and returns TV schedules through Pipeworx.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses a mutable remote npm package through mcp-remote@latest.

Mitigation: Prefer a pinned and reviewed version of mcp-remote before installing or deploying the connector.

Risk: Requests route through a third-party Pipeworx gateway.

Mitigation: Use minimal filesystem and environment access, and avoid sending personal or confidential search content unless the third-party trust boundary is acceptable.

## Reference(s):

- [Pipeworx Movies Pack](https://pipeworx.io/packs/movies)
- [ClawHub Skill Page](https://clawhub.ai/b-gutman/skills/pipeworx-movies)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands]

**Output Format:** [Markdown with JSON configuration and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MCP connection guidance for an agent; no API key is indicated by the artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
