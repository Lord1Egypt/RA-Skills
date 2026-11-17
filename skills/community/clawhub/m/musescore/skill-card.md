## Description:

Search MuseScore sheet music and read score metadata via MCP. Triggers on phrases like "find sheet music for", "search MuseScore for", "is there a free arrangement of", "what's the license on this MuseScore score", "how many pages is", or any request involving MuseScore scores, arrangements, or sheet-music metadata. Requires musescore-mcp installed and the ContextMint Bridge browser extension active with a signed-in musescore.com tab (see Setup).

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find sheet music, inspect score metadata, and retrieve available score files or page renders through a signed-in MuseScore browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve score files and perform local file conversion; the security review noted that some local path references could not be resolved.

Mitigation: Review score access and the intended output location before retrieval, and check local path references and file handling before enabling file tools.

## Reference(s):

- [MuseScore](https://musescore.com)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [ContextMint Bridge source](https://github.com/nullnet-app/contextmint-bridge)

## Skill Output:

**Output Type(s):** [JSON, Files, Guidance]

**Output Format:** [Structured score metadata, file links, and optionally PDF, SVG, or score files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Download availability depends on score access; hosted and local delivery provide different file outputs.]

## Skill Version(s):

1.3.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
