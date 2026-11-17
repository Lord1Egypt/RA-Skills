## Description:

Use this skill for Weatherbit requests that involve searching and reading data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users retrieve current observations and daily or hourly forecasts for a location through their connected Weatherbit account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified software and make broader agent changes without clear user approval.

Mitigation: Review setup, install a verified CLI release yourself, and require approval before software installation; consider disabling managed-skill synchronization with the documented OO_SKILLS_SYNC_DISABLED setting.

Risk: OOMOL mediates Weatherbit requests and credentials, and its hosted service implementation has not been verified.

Mitigation: Review OOMOL's handling of requests and credentials before connecting the Weatherbit account.

## Reference(s):

- [Weatherbit homepage](https://www.weatherbit.io)
- [Weatherbit current weather API documentation](https://www.weatherbit.io/api/weather-current)
- [oo CLI command and environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Weather observations or forecast data returned as JSON, which the agent can summarize in text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Location-specific current observations, daily forecasts, or hourly forecasts.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
