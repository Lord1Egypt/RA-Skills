## Description:

One-day weather brief from Open-Meteo (no API key): high/low, rain hours, sunset, and dry daylight windows to get outside, optionally fitted into free gaps in your calendar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anvacy](https://clawhub.ai/user/anvacy)

### License/Terms of Use:

MIT-0

## Use Case:

People using an assistant can get today's or tomorrow's conditions, rain hours, sunset, and dry outdoor windows. If free-time gaps are supplied, the skill can fit outdoor windows to those times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends supplied location coordinates to Open-Meteo and keeps a local forecast cache for fallback.

Mitigation: Use coordinates you are comfortable sending to the service, and review the local cache behavior for your environment.

Risk: The security review is incomplete, and the skill does not declare its tool scope.

Mitigation: Inspect the full skill and confirm its permissions fit the environment before deployment.

## Reference(s):

- [Open-Meteo](https://open-meteo.com)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON forecast data used to produce a concise natural-language weather brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes temperature, rain periods, sunrise and sunset, and dry outdoor windows; windows can be limited to supplied free-time gaps.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
