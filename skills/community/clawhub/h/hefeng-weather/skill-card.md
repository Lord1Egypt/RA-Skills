## Description:

Queries QWeather for current weather, hourly and daily forecasts, and minute-level precipitation for a specified city.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronjager92](https://clawhub.ai/user/aaronjager92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to answer weather requests in Chinese chat or command-line workflows by querying configured QWeather endpoints for a requested city.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A QWeather API key is required and could be exposed if stored carelessly.

Mitigation: Prefer HEFENG_WEATHER_API_KEY, keep local config files out of shared artifacts, and install only if providing a QWeather key is acceptable.

Risk: The setup text contains a conflicting API key link.

Mitigation: Use the official QWeather account portal at https://id.qweather.com/ and avoid the minimaxi.com link.

Risk: The Python requests dependency is not pinned.

Mitigation: Pin dependencies in managed environments before deployment.

## Reference(s):

- [Artifact setup and usage reference](artifact/references/README.md)
- [QWeather account portal](https://id.qweather.com/)
- [ClawHub skill page](https://clawhub.ai/aaronjager92/skills/hefeng-weather)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples; command-line output is plain text weather summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a QWeather API key configured through HEFENG_WEATHER_API_KEY or config.txt.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
