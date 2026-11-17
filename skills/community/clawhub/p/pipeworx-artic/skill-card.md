## Description:

Explore the Art Institute of Chicago's collection — artworks, artists, and exhibitions via the ARTIC public API

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, and developers use this skill to query Art Institute of Chicago artworks, artists, and exhibitions for education, trip planning, collection lookup, and downstream analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup runs an unpinned npm package automatically, creating a supply-chain review risk.

Mitigation: Pin mcp-remote to a reviewed exact version and avoid automatic install confirmation where practical.

Risk: The runtime depends on the Pipeworx gateway for API behavior.

Mitigation: Run the MCP process with limited filesystem and environment access before using it in normal workflows.

## Reference(s):

- [Pipeworx ARTIC pack homepage](https://pipeworx.io/packs/artic)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include artwork metadata, artist details, exhibition records, image URLs, and IIIF URL guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
