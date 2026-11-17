## Description:

Provides real-time Swiss public transport station search, route planning, schedules, and live departure boards for trains, buses, and trams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and transit-focused agents use this skill to look up Swiss stations, plan routes, and retrieve live departures for trains, buses, and trams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided station and route queries are sent to a disclosed third-party MCP gateway.

Mitigation: Avoid entering sensitive private locations or travel plans unless sharing them with that service is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-swisstransport)
- [Swiss transport MCP endpoint](https://gateway.pipeworx.io/swisstransport/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include station identifiers, coordinates, route timings, transfers, platforms, delays, and live departure details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
