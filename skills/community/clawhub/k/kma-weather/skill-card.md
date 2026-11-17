## Description:

Get weather from Korea Meteorological Administration (KMA), including current conditions, 3-10 day forecasts, and weather warnings or advisories for South Korea.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steamb23](https://clawhub.ai/user/steamb23)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to fetch official South Korea weather observations, short-term forecasts, mid-term outlooks, and nationwide weather warning summaries through KMA public APIs.

### Deployment Geography for Use:

South Korea

## Known Risks and Mitigations:

Risk: KMA_SERVICE_KEY is a credential and may appear in request URLs if users capture or share raw API requests.

Mitigation: Store the key only in the configured environment variable and redact service keys or full request URLs from logs, screenshots, and shared transcripts.

Risk: The skill is limited to South Korea weather data and may return no data or misleadingly broad results for unsupported coordinates or regions.

Mitigation: Confirm that latitude, longitude, or region inputs are within South Korea and prefer the short-term grid forecast for precise local conditions.

Risk: Forecasts and warning summaries may be returned in Korean, which can lead to interpretation errors for non-Korean readers.

Mitigation: Preserve official Korean terms where safety-relevant and translate or summarize them carefully when presenting results to users.

Risk: Several KMA endpoints are intentionally not implemented, including detailed warning messages and some mid-term land, temperature, and sea forecasts.

Mitigation: Use the implemented endpoint list to set expectations and consult official KMA services directly when unsupported detail is required.

## Reference(s):

- [Korea Weather ClawHub Page](https://clawhub.ai/steamb23/skills/kma-weather)
- [KMA Short-term Forecast API](https://www.data.go.kr/data/15084084/openapi.do)
- [KMA Weather Warnings API](https://www.data.go.kr/data/15000415/openapi.do)
- [KMA Mid-term Forecast API](https://www.data.go.kr/data/15059468/openapi.do)
- [Short-term Forecast API Reference](references/api-forecast.md)
- [Weather Warnings API Reference](references/api-warnings.md)
- [Mid-term Forecast API Reference](references/api-midterm.md)
- [Category Codes Reference](references/category-codes.md)
- [Implementation Status](implement-status.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON from Python CLI commands, usually embedded in agent guidance or Markdown responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and KMA_SERVICE_KEY; outputs may include Korean weather terminology and official KMA warning text.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
