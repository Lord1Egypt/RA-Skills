## Description:

Current weather and forecasts with web_fetch, falling back to wttr.in curl for locations, rain, temperature, travel planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to answer requests for current conditions, rain and temperature checks, short-range forecasts, and weather context for travel planning. The user supplies a city, region, airport code, or coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups may send the requested location to wttr.in, an external service.

Mitigation: Use a city-level location when it is sufficient for the forecast.

## Reference(s):

- [wttr.in help](https://wttr.in/:help)
- [Weather skill on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-weather)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Concise natural-language weather summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes current conditions and forecast details returned by wttr.in.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
