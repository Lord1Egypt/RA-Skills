## Description:

Search Project Gutenberg's 70,000+ free ebooks by title, author, topic, or popularity via Gutendex.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search public-domain ebooks, retrieve book details, browse popular Project Gutenberg titles, and collect download links in formats such as EPUB, plain text, and HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Book search queries are sent to the Pipeworx gateway.

Mitigation: Avoid sensitive queries and confirm external data-sharing expectations before enabling the connector.

Risk: The documented MCP setup runs mcp-remote@latest through npm, so the resolved bridge package can change over time.

Mitigation: Pin mcp-remote to a reviewed version or install it through a locked dependency workflow before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/b-gutman/skills/pipeworx-gutendex)
- [Pipeworx Gutendex Homepage](https://pipeworx.io/packs/gutendex)
- [Pipeworx Gutendex MCP Gateway](https://gateway.pipeworx.io/gutendex/mcp)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON MCP configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns book metadata, subjects, download counts, and format links when called through the MCP gateway.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
