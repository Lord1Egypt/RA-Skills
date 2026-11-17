## Description:

OpenWeather (openweathermap.org). Use this skill for ANY OpenWeather request — reading, creating, updating, and deleting data. Whenever a task involves OpenWeather, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected OpenWeather account can retrieve current conditions, forecasts, air-pollution and UV data, resolve locations, and manage weather stations. The skill guides them to inspect each action's input schema before sending a request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified third-party software without asking the user.

Mitigation: Review installer behavior, install the CLI yourself from a verified release, and avoid automatically executing installer commands.

Risk: Weather-station actions can create, update, submit, or delete account data.

Mitigation: Confirm the exact payload and effect before write actions, and get explicit approval before deletion.

## Reference(s):

- [OpenWeather](https://openweathermap.org)
- [OpenWeather API documentation](https://openweathermap.org/api)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Base64 PNG data]

**Output Format:** [Structured OpenWeather API results and text summaries; weather-map tiles as Base64-encoded PNG data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available result fields depend on the selected OpenWeather action.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
