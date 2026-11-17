## Description:

Search AccuWeather locations and retrieve current conditions and daily or hourly forecasts through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to find AccuWeather locations and retrieve current conditions or forecasts through an existing OOMOL AccuWeather connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute changing remote code, and startup may write skills into other agents' directories.

Mitigation: Install a verified oo CLI release yourself rather than running an automatic remote installer. Set OO_SKILLS_SYNC_DISABLED=1 to prevent startup writes to other agents' skill directories.

Risk: OOMOL mediates weather requests and connected credentials; the hosted connector implementation was not inspected.

Mitigation: Use an OOMOL connection intended for this service and review the CLI and connection setup before connecting an account.

## Reference(s):

- [AccuWeather API Documentation](https://developer.accuweather.com/core-weather)
- [AccuWeather](https://www.accuweather.com)
- [oo CLI Environment Variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON connector requests and responses, with weather information summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weather information depends on the selected AccuWeather location and forecast action.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
