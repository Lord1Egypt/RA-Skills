## Description:

Provides precise sunrise, sunset, dawn, dusk, solar noon, golden hour, and day length times for any location and date worldwide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve sunrise, sunset, twilight, golden hour, solar noon, and day length information for a supplied latitude and longitude, optionally for a specific date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location and date requests are sent to the disclosed PipeWorx gateway service.

Mitigation: Avoid submitting precise private coordinates when location privacy matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-sunrisesunset)
- [PipeWorx sunrise/sunset MCP gateway](https://gateway.pipeworx.io/sunrisesunset/mcp)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands, guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns sun-time values for requested coordinates and dates through a disclosed remote service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
