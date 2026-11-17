## Description:

Get current weather data, forecasts, and weather information from OpenWeatherMap API for location-based weather queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philiplawlor](https://clawhub.ai/user/philiplawlor)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve and format current weather and forecast information from OpenWeatherMap for cities or coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups send the queried city or coordinates and the OpenWeatherMap API key to OpenWeatherMap.

Mitigation: Use the OPENWEATHERMAP_API_KEY environment variable, avoid precise coordinates unless needed, and avoid sharing real keys in logs or prompts.

Risk: The skill may ask the user for an API key if it is not available in the environment or ~/.openweathermap.

Mitigation: Configure OPENWEATHERMAP_API_KEY or ~/.openweathermap before use so users do not need to paste credentials into an agent conversation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/philiplawlor/skills/openweathermap)
- [OpenWeatherMap API keys](https://home.openweathermap.org/api_keys)
- [OpenWeatherMap current weather API endpoint](https://api.openweathermap.org/data/2.5/weather)
- [OpenWeatherMap forecast API endpoint](https://api.openweathermap.org/data/2.5/forecast)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Markdown]

**Output Format:** [Markdown with API request examples and formatted weather summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenWeatherMap request URLs, unit guidance, and weather fields such as temperature, humidity, wind, sunrise, and sunset.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
