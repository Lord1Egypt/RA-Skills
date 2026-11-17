## Description:

Fetch weather forecasts, current conditions, historical weather, and air quality with the free Open-Meteo API (no API key). Use for any weather, temperature, rain, wind, UV, sunrise/sunset, air quality, or climate data task, even if Open-Meteo isn't mentioned.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanookai](https://clawhub.ai/user/nanookai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to fetch and interpret Open-Meteo weather data, including current conditions, forecasts, historical weather, air quality, marine data, and climate endpoints. It helps agents produce concise weather answers, API requests, code snippets, and shell commands without requiring an API key for normal use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather place names or coordinates may be sent to Open-Meteo when the skill or bundled script fetches data.

Mitigation: Avoid including sensitive personal context in place-name queries; send only the location or coordinates needed for the weather request.

Risk: Weather, air-quality, historical, marine, and climate responses can be misread as exact local observations or guarantees.

Mitigation: Present results as Open-Meteo API data, include units and timestamps, and choose the documented endpoint for the user's forecast, historical, or climate task.

## Reference(s):

- [ClawHub Open-Meteo API Skill Page](https://clawhub.ai/nanookai/skills/open-meteo-api)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search)
- [Open-Meteo Historical Weather API](https://archive-api.open-meteo.com/v1/archive)
- [Open-Meteo Air Quality API](https://air-quality-api.open-meteo.com/v1/air-quality)
- [Open-Meteo Other APIs](references/other-apis.md)
- [Open-Meteo Forecast API Variable Catalog](references/weather-variables.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, API calls, JSON, Guidance]

**Output Format:** [Markdown with inline code blocks, shell commands, API URLs, and optional JSON output from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Open-Meteo endpoints over HTTPS and return formatted weather text or raw JSON when requested.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
