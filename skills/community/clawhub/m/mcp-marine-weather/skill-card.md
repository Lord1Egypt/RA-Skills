## Description:

Marine weather forecasts from NOAA api.weather.gov, including current conditions, multi-day forecasts, and marine weather warnings without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haveblue997](https://clawhub.ai/user/haveblue997)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this MCP server to check NOAA marine weather for sailing, offshore activity, coastal events, and pre-departure briefings for supported U.S. and territorial waters.

### Deployment Geography for Use:

United States and U.S. territories

## Known Risks and Mitigations:

Risk: The documented setup runs an unpinned third-party package through npx with normal local code execution authority.

Mitigation: Pin the npx command to a reviewed exact package version and confirm the package identity before installation.

Risk: Weather functionality depends on NOAA service availability and coverage.

Mitigation: Use the output as a planning aid and verify safety-critical marine decisions with official weather channels.

## Reference(s):

- [NOAA Weather API](https://api.weather.gov)
- [ClawHub skill page](https://clawhub.ai/haveblue997/skills/mcp-marine-weather)

## Skill Output:

**Output Type(s):** [Text, Configuration]

**Output Format:** [JSON serialized as MCP text content, plus MCP server setup configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts latitude and longitude coordinates; returns current conditions, forecast periods, and marine-relevant warnings.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
