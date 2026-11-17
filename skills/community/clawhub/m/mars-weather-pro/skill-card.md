## Description:

Get current weather and forecasts (no API key required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mars82311111](https://clawhub.ai/user/mars82311111)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for current weather, compact weather summaries, multi-day forecasts, and JSON weather data without configuring an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups may send requested city names, airport codes, or coordinates to wttr.in or Open-Meteo.

Mitigation: Use only locations or coordinates that are appropriate to share with external weather services.

Risk: The PNG example writes to a fixed /tmp/weather.png path.

Mitigation: Save downloaded images to a caller-controlled path to avoid accidental overwrite or path confusion.

## Reference(s):

- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo documentation](https://open-meteo.com/en/docs)
- [Open-Meteo forecast API example](https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for the documented command examples; no API key is required.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
