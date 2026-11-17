## Description:

Provides real-time and historical USGS streamflow and gage height data for rivers, creeks, and streams across the United States.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find USGS monitoring sites, retrieve current streamflow and gage height readings, and request historical daily mean streamflow values for water monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: USGS water-data queries are routed through the listed Pipeworx gateway.

Mitigation: Confirm the gateway is acceptable for the deployment environment and avoid sending private information in tool arguments.

## Reference(s):

- [Pipeworx USGS Water skill page](https://clawhub.ai/b-gutman/skills/pipeworx-usgswater)
- [Publisher profile](https://clawhub.ai/user/b-gutman)
- [Pipeworx USGS Water MCP endpoint](https://gateway.pipeworx.io/usgswater/mcp)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool responses include site identifiers, coordinates, timestamps, data quality flags, discharge, gage height, and daily mean streamflow values when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
