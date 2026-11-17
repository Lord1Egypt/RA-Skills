## Description:

Search, summarize, and explore the structure of English Wikipedia articles with full-text search, section information, and random article retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search English Wikipedia, retrieve article summaries, inspect article sections, and fetch random articles through a Pipeworx-hosted MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wikipedia search terms and requested article titles are sent to the third-party Pipeworx gateway.

Mitigation: Do not include secrets or private context in queries; install only when this routing is acceptable.

Risk: Wikipedia content may be incomplete, outdated, or unsuitable as the sole source for high-stakes facts.

Mitigation: Verify important facts against official Wikimedia pages or other authoritative sources before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-wikipedia)
- [Pipeworx Wikipedia MCP gateway](https://gateway.pipeworx.io/wikipedia/mcp)
- [Publisher profile](https://clawhub.ai/user/brucegutman)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP tool responses can include article titles, snippets, summaries, section metadata, thumbnails, and article links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
