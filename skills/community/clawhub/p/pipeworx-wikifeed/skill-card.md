## Description:

Provides curated Wikipedia content including historical events on a date, daily featured articles, most read pages, and picture of the day.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Wikipedia-style daily and date-based content, including historical events, featured articles, most-read pages, and picture-of-the-day metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup queries are sent to the disclosed pipeworx.io MCP gateway.

Mitigation: Confirm the endpoint is acceptable before installation and avoid sending secrets or private data as tool arguments.

Risk: Returned Wikipedia-style content can be time-sensitive or incomplete for consequential decisions.

Mitigation: Treat returned content as informational and verify important facts against authoritative sources before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-wikifeed)
- [Wikifeed MCP gateway](https://gateway.pipeworx.io/wikifeed/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with curl examples and MCP configuration JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns Wikipedia content selectors, extracts, URLs, image URLs, thumbnails, and view-count-oriented results depending on the selected tool.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
