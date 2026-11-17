## Description:

Search and look up books via Open Library, including titles, authors, ISBNs, and cover image URLs from the world's largest open book catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to search for books, retrieve ISBN-based book metadata, and fetch author details for reading lists, catalog enrichment, and recommendation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP configuration runs mcp-remote from the latest npm tag, so the installed bridge code can change between installs.

Mitigation: Pin mcp-remote to a reviewed exact version and install it through a controlled package process before enabling the skill.

Risk: The skill depends on a remote Pipeworx books service for MCP tool execution.

Mitigation: Use it only where that remote service is acceptable and run the MCP server with limited filesystem and environment access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-books)
- [Pipeworx Books Pack](https://pipeworx.io/packs/books)
- [Pipeworx Books MCP Endpoint](https://gateway.pipeworx.io/books/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON MCP configuration, bash examples, and structured JSON book or author results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for the documented example and uses a remote Pipeworx MCP service through an npm-based bridge.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
