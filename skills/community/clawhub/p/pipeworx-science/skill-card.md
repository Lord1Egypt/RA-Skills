## Description:

Provides live science data feeds for ISS location, recent earthquakes, local air quality, and NASA Astronomy Picture of the Day content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query current science information from a Pipeworx-hosted MCP gateway, including orbital position, earthquake events, air quality readings, and astronomy media metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Science queries and location parameters are routed to the remote Pipeworx gateway.

Mitigation: Use the skill only when this routing is acceptable, and avoid sending precise personal coordinates if that location is sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-science)
- [Pipeworx science MCP endpoint](https://gateway.pipeworx.io/science/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and example shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include live science measurements, coordinates, image URLs, explanations, and source-specific metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
