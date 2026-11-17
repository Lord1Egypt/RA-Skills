## Description:

Fetch xkcd comics by number, latest release, or random selection, returning comic metadata including title, alt text, image URL, date, transcript, and permalink.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve xkcd comics through the Pipeworx xkcd MCP gateway for citation, reference, or lightweight contextual enrichment in agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends xkcd lookup requests to the Pipeworx gateway and receives comic metadata through that third-party service.

Mitigation: Install and use it only where that external service dependency is acceptable.

Risk: Returned titles, transcripts, alt text, and URLs are external content.

Mitigation: Treat returned comic fields as data for review or display, not as agent instructions.

## Reference(s):

- [Pipeworx xkcd skill on ClawHub](https://clawhub.ai/brucegutman/skills/pipeworx-xkcd)
- [Publisher profile](https://clawhub.ai/user/brucegutman)
- [Pipeworx xkcd MCP gateway](https://gateway.pipeworx.io/xkcd/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns externally sourced comic fields such as title, alt text, transcript, image URL, date, and permalink.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
