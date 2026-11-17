## Description:

UK postcode lookup skill for retrieving coordinates, administrative areas, parliamentary constituencies, NHS regions, neighbouring postcodes, validation results, and random valid postcodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query UK postcode geography and validation through a Pipeworx-hosted MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Postcode queries are sent to a Pipeworx-hosted MCP endpoint, which may expose location-related data to that external service.

Mitigation: Avoid submitting sensitive location data unless the service and its data handling practices are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-postcodes)
- [Pipeworx postcodes MCP endpoint](https://gateway.pipeworx.io/postcodes/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with JSON configuration and inline bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Postcode lookups are fulfilled by an external Pipeworx-hosted MCP endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-04-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
