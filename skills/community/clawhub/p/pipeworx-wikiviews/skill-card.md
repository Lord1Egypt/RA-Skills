## Description:

Provides Wikipedia pageview data including daily views for specific articles, top articles by date, and aggregate English Wikipedia traffic trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Wikipedia article, top-page, and project-wide pageview analytics through the disclosed Pipeworx wikiviews MCP endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wikipedia pageview queries are sent to the disclosed Pipeworx gateway rather than directly to Wikimedia.

Mitigation: Avoid sending sensitive private research topics through this skill when that traffic exposure matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-wikiviews)
- [Pipeworx wikiviews MCP endpoint](https://gateway.pipeworx.io/wikiviews/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Wikipedia pageview counts, ranked article lists, and aggregate traffic trend data from a disclosed external MCP endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
