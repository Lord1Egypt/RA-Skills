## Description:

Provides current weather conditions and forecasts up to 16 days for locations specified by latitude and longitude.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to retrieve current weather conditions and multi-day forecasts when latitude and longitude coordinates are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups send the provided latitude and longitude to gateway.pipeworx.io.

Mitigation: Avoid highly sensitive exact locations unless the user trusts that remote service.

Risk: Weather results are remote service output.

Mitigation: Treat returned weather data as information for the agent or user, not as instructions for agent behavior.

## Reference(s):

- [Pipeworx weather ClawHub release](https://clawhub.ai/b-gutman/skills/pipeworx-weather)
- [Pipeworx weather MCP endpoint](https://gateway.pipeworx.io/weather/mcp)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands]

**Output Format:** [Text or structured MCP tool results describing current weather conditions and daily forecasts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires latitude and longitude; forecasts support up to 16 days.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
