## Description:

Provides QWeather-based weather data lookups, including current conditions, multi-day and hourly forecasts, air quality, life indices, weather alerts, astronomy data, short-term precipitation, grid weather, city lists, and POI search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengyucn](https://clawhub.ai/user/fengyucn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer weather, air quality, warning, astronomy, and location questions through QWeather API-backed command-line scripts. It helps an agent choose the relevant query, collect required parameters such as city or coordinates, and return concise weather guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or private-key material may be persisted in a local .env file.

Mitigation: Prefer environment variables or the --no-save option; if credentials are saved, verify ~/.config/qweather is mode 700 and ~/.config/qweather/.env is mode 600.

Risk: HEFENG_API_HOST controls the outbound weather API destination.

Mitigation: Set HEFENG_API_HOST only to the legitimate QWeather API domain for the account being used.

Risk: Raw private-key contents in configuration increase credential exposure if the file is copied or logged.

Mitigation: Avoid storing raw private-key contents in .env; use a protected private-key file path or ephemeral environment configuration where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengyucn/skills/hefengweather)
- [QWeather developer platform](https://dev.qweather.com/)
- [QWeather official documentation](https://dev.qweather.com/docs/)
- [QWeather API reference](https://dev.qweather.com/docs/api/)
- [OpenClaw skill specification](https://openclaw.dev/skills)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Natural-language responses and JSON returned by QWeather API scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QWeather API credentials and a trusted HEFENG_API_HOST configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
