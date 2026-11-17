## Description:

Get today's high, low, and maximum rain chance for a user-selected public location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattheqd](https://clawhub.ai/user/mattheqd)

### License/Terms of Use:

MIT-0

## Use Case:

An agent uses this skill to look up today's forecast for a user's selected public location and report the date, location, Fahrenheit high and low, maximum rain chance, and source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner verdict is benign with medium confidence, but only half of the components were inspected and executable behavior was not fully interpreted.

Mitigation: Review forecast.mjs and scan the full release before use.

Risk: The skill does not declare its tool scope, and the host's runtime permissions are unknown.

Mitigation: Run with minimal permissions, allowing only the HTTPS access needed for Open-Meteo.

Risk: The selected public location is sent to Open-Meteo's geocoding and forecast services.

Mitigation: Use only a location the user is comfortable sharing with those services.

## Reference(s):

- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)
- [ClawHub release page](https://clawhub.ai/mattheqd/skills/open-meteo-daily-weather-a3)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Concise daily weather summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One forecast day in the location's time zone, with temperatures in Fahrenheit.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
