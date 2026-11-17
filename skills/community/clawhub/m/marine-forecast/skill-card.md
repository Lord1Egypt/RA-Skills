## Description:

Marine and sailing weather via Open-Meteo. Waves, swell, sea temperature, wind, tides, ocean currents, and sailing assessments. Free, no API key, global coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexissan](https://clawhub.ai/user/alexissan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request marine conditions and sailing forecasts for coastal or open-water locations. The agent fetches Open-Meteo marine and weather data, combines the results, and presents a concise sailing briefing with conditions, warnings, and activity suitability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forecast requests send queried coordinates and timezone to Open-Meteo.

Mitigation: Avoid using the skill for locations considered sensitive, and disclose that approximate coordinates are shared with the external weather API.

Risk: Marine forecasts and derived tide estimates may be less precise near harbors, bays, or coastal grid boundaries.

Mitigation: Treat the briefing as planning guidance, verify safety-critical decisions against local marine forecasts and notices, and prefer current or daily summaries when detailed hourly arrays are unnecessary.

## Reference(s):

- [Open-Meteo Marine Weather API documentation](https://open-meteo.com/en/docs/marine-weather-api)
- [ClawHub skill page](https://clawhub.ai/alexissan/skills/marine-forecast)
- [Publisher profile](https://clawhub.ai/user/alexissan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline shell commands and structured weather briefings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JSON responses from Open-Meteo and may include condition ratings, warnings, tide estimates, and activity suitability.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
