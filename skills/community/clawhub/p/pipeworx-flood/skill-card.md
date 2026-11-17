## Description:

River discharge and flood forecasts for any location - up to 92 days ahead via Open-Meteo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and risk teams use this skill to request river discharge and flood forecasts for locations of interest, supporting preparedness, insurance assessment, agriculture planning, and monitoring of flood-prone areas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup runs a mutable npm package through npx, which can change between installs.

Mitigation: Review before installing, pin mcp-remote to a specific reviewed version, and run the MCP bridge in a restricted environment.

Risk: Using the flood forecast tools sends requested coordinates to the Pipeworx gateway and upstream forecast service.

Mitigation: Avoid submitting sensitive private locations unless sharing those coordinates is acceptable.

## Reference(s):

- [Pipeworx Flood homepage](https://pipeworx.io/packs/flood)
- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-flood)
- [Pipeworx Flood MCP endpoint](https://gateway.pipeworx.io/flood/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks; forecast service responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forecasts include daily discharge values and may include mean, median, and maximum discharge metrics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
