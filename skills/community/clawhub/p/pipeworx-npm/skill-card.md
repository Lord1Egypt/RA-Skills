## Description:

npm MCP wraps the npm Registry API without requiring authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to connect an MCP server that searches npm packages, retrieves package metadata, and checks package download counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs the Pipeworx remote MCP bridge locally through an unpinned npm package.

Mitigation: Review the bridge before enabling it, prefer pinning mcp-remote to an exact reviewed version, and run the MCP process with least-privilege filesystem, environment, and network access.

## Reference(s):

- [Pipeworx npm pack](https://pipeworx.io/packs/npm)
- [Pipeworx](https://pipeworx.io)
- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-npm)
- [Server-resolved provenance](unavailable)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with JSON configuration and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MCP setup guidance and tool-use guidance for npm package search, package metadata lookup, and download count retrieval.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
