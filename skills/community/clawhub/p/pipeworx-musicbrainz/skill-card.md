## Description:

MusicBrainz MCP connector that wraps MusicBrainz Web Service v2 without requiring authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search MusicBrainz artist and release data through a Pipeworx-hosted MCP connector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses an unpinned npm package for mcp-remote.

Mitigation: Review before installing and prefer a pinned, reviewed mcp-remote version.

Risk: Music searches are routed through Pipeworx rather than directly to MusicBrainz.

Mitigation: Run with limited filesystem and environment access, and avoid sending private or identifying context in searches.

## Reference(s):

- [Pipeworx MusicBrainz Pack](https://pipeworx.io/packs/musicbrainz)
- [ClawHub Skill Page](https://clawhub.ai/b-gutman/skills/pipeworx-musicbrainz)

## Skill Output:

**Output Type(s):** [API Calls, Configuration, Guidance]

**Output Format:** [Markdown with JSON configuration and tool names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a third-party Pipeworx gateway for MusicBrainz MCP requests.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
