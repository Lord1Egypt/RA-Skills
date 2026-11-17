## Description:

Get current weather and forecasts with no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mars82311111](https://clawhub.ai/user/mars82311111)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to get current weather, compact condition summaries, full forecasts, and JSON weather data for chosen locations through public weather services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location names or coordinates requested through the skill are sent to public weather services.

Mitigation: Avoid querying highly sensitive precise locations when that privacy tradeoff is unacceptable.

Risk: Weather responses depend on availability and behavior of wttr.in and Open-Meteo.

Mitigation: Use Open-Meteo as a fallback when wttr.in output is unavailable or unsuitable for programmatic use.

## Reference(s):

- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true)
- [Open-Meteo documentation](https://open-meteo.com/en/docs)
- [ClawHub skill page](https://clawhub.ai/mars82311111/skills/mars-weather-ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for command examples; no API key is required.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
