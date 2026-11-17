## Description:

Search and explore 500,000+ artworks in the Metropolitan Museum of Art's open-access collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, researchers, and developers use this skill to search Met Museum artworks, inspect object details, and retrieve structured metadata for educational content, recommendations, or collection comparison workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs `mcp-remote@latest`, so installs may pick up unreviewed package changes.

Mitigation: Pin and review the `mcp-remote` version or use a controlled local install before deployment.

Risk: The skill connects to a remote MCP gateway for artwork queries.

Mitigation: Run the MCP process with only the filesystem, environment, and network access needed for the documented art-search workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-art)
- [Pipeworx Art homepage](https://pipeworx.io/packs/art)
- [Pipeworx Art MCP endpoint](https://gateway.pipeworx.io/art/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include artwork metadata such as titles, artists, dates, media, departments, image URLs, object URLs, gallery locations, provenance, and exhibition history.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
