## Description:

Aviation weather data for METAR observations, TAF forecasts, and nearby station discovery via an L402 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haveblue997](https://clawhub.ai/user/haveblue997)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and aviation operators can use this MCP server to retrieve METAR observations, TAF forecasts, and nearby weather station data for flight planning, airport weather checks, and safety briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance can run unpinned npm code, and artifact documentation names inconsistent npm packages and environment variables.

Mitigation: Confirm the authoritative npm package, pin an exact audited version, and configure only the required environment variables before installation.

Risk: Repeated tool calls may create L402 micropayment costs without clear spending controls.

Mitigation: Review L402 pricing and enforce spending limits or approval controls before allowing automated repeated calls.

Risk: Aviation weather output may be used in operational flight-planning decisions.

Mitigation: Treat responses as advisory agent output and verify weather data against authoritative aviation sources before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haveblue997/skills/mcp-aviation-weather)
- [Configured L402 API base URL](https://api.nautdev.com)
- [Pricing details referenced by artifact README](https://github.com/Blue-Trianon-Ventures)

## Skill Output:

**Output Type(s):** [text, JSON, configuration]

**Output Format:** [MCP tool responses containing JSON text, plus MCP server configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool calls accept ICAO station identifiers or latitude, longitude, and optional radius; requests use a configurable L402 API base URL.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
