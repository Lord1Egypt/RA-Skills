## Description:

Get current weather and forecasts (no API key required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mars82311111](https://clawhub.ai/user/mars82311111)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to get current weather and forecast guidance for a city, airport code, or coordinates without configuring an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather queries are sent to wttr.in or Open-Meteo and may reveal the requested city, airport code, or coordinates to those providers.

Mitigation: Avoid sending sensitive locations, review generated commands before execution, and use only locations that are acceptable to disclose to public weather services.

Risk: The skill depends on public weather services and curl, so availability and response formats can affect results.

Mitigation: Confirm curl is installed, inspect returned weather data before acting on it, and fall back from wttr.in to Open-Meteo when needed.

## Reference(s):

- [wttr.in Help](https://wttr.in/:help)
- [Open-Meteo Forecast API Documentation](https://open-meteo.com/en/docs)
- [MarsAI Weather Forecast on ClawHub](https://clawhub.ai/mars82311111/skills/marsai-weather-forecast)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown with inline bash code blocks and optional JSON weather responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and makes outbound requests to public weather services.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
