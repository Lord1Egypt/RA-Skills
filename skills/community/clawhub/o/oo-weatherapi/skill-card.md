## Description:

Use WeatherAPI through the connected oo CLI to search locations and retrieve current weather, forecasts, astronomy, and timezone data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill with their connected OOMOL account to search WeatherAPI locations and retrieve current conditions, forecasts, astronomy, or timezone information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, setup instructions run an online installer without a separate approval step; automated installation or setup changes may affect other agent skills.

Mitigation: Install a verified, pinned CLI before use and review any changes it makes to other agents' skills. Assess whether you trust OOMOL to mediate WeatherAPI access and location queries.

## Reference(s):

- [WeatherAPI](https://www.weatherapi.com)
- [WeatherAPI Documentation](https://www.weatherapi.com/docs/)

## Skill Output:

**Output Type(s):** [JSON data, Weather and location information]

**Output Format:** [Structured JSON connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned data depends on the selected action, location query, and optional date.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
