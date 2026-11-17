## Description:

AnimeQuotes MCP wraps animechan.io for free, unauthenticated anime quote queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to query anime quote information through the Pipeworx AnimeQuotes MCP gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suggested MCP client setup runs an unpinned npm bridge package.

Mitigation: Pin mcp-remote to a reviewed exact version, use a lockfile or controlled environment, and limit the MCP process's filesystem, environment-variable, and network access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-animequotes)
- [Pipeworx AnimeQuotes homepage](https://pipeworx.io/packs/animequotes)
- [Pipeworx homepage](https://pipeworx.io)
- [Pipeworx AnimeQuotes MCP endpoint](https://gateway.pipeworx.io/animequotes/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with JSON-RPC examples and MCP client configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns JSON-RPC 2.0 responses from the Pipeworx AnimeQuotes gateway.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
