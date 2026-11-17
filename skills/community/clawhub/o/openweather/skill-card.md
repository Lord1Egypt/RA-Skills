## Description:

Get current weather, hourly forecasts, and 8-day daily forecasts for any location worldwide using OpenWeather One Call API 3.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joshua-ensley](https://clawhub.ai/user/joshua-ensley)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent answer weather questions with current conditions, hourly forecasts, and daily forecasts for a requested location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an OpenWeather API key and sends that key to OpenWeather endpoints.

Mitigation: Use a key scoped for OpenWeather access and monitor quota or billing activity.

Risk: Requested locations, including a configured default location, are sent to OpenWeather over HTTPS.

Mitigation: Avoid configuring or requesting sensitive locations unless that disclosure is acceptable.

Risk: Weather responses depend on OpenWeather account activation, quota, and API availability.

Mitigation: Confirm One Call API 3.0 is enabled for the key and handle 401, 429, and server errors as user-visible API failures.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/joshua-ensley/skills/openweather)
- [OpenWeather One Call API 3.0 Quick Reference](api-reference.md)
- [OpenWeather API](https://openweathermap.org/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Plain text CLI output with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENWEATHER_API_KEY; weather requests send the requested or configured default location to OpenWeather over HTTPS.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
