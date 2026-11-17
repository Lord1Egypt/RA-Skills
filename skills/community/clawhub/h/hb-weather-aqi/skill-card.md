## Description:

Provides real-time weather and air quality index (AQI) data for a requested location using Open-Meteo and WAQI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guchigangz](https://clawhub.ai/user/guchigangz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer weather and air-quality questions for a named location. It can return either readable text or JSON for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested locations are sent to external weather, geocoding, and air-quality APIs.

Mitigation: Use only when sharing the searched location with Open-Meteo and WAQI is acceptable.

Risk: The WAQI API token is required for air-quality lookup and may appear in request URLs.

Mitigation: Treat the token as a secret and avoid environments where outbound request URLs are broadly logged.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guchigangz/skills/hb-weather-aqi)
- [Publisher profile](https://clawhub.ai/user/guchigangz)
- [Open-Meteo geocoding endpoint](https://geocoding-api.open-meteo.com/v1/search)
- [Open-Meteo forecast endpoint](https://api.open-meteo.com/v1/forecast)
- [WAQI geo feed endpoint](https://api.waqi.info/feed/geo:)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Plain text weather and AQI summary, or formatted JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a requested location and a WAQI API token supplied through the environment.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
