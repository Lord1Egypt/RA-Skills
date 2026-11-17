## Description:

KMA short-term forecast API - ultra-short-term observation/forecast, short-term forecast.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sw326](https://clawhub.ai/user/sw326)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve and summarize South Korea weather forecasts from KMA data.go.kr APIs, with optional AirKorea air-quality context. It supports current conditions, short-range forecasts, daily briefings, and KMA grid-coordinate conversion.

### Deployment Geography for Use:

Global, for South Korea weather data coverage.

## Known Risks and Mitigations:

Risk: One script reads a data.go.kr API key from a hard-coded other-user home path, creating a credential-scope and portability risk.

Mitigation: Before use, update the script to read the invoking user's configured key and store that key in a 0700 directory with 0600 file permissions.

Risk: A previously exposed API key may have been visible through shell history, process monitoring, or local file access.

Mitigation: Rotate the key before deployment if it may have been exposed, then reconfigure the skill with the replacement key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sw326/skills/kma-weather-korea)
- [KMA Short-Term Forecast OpenAPI](https://www.data.go.kr/data/15084084/openapi.do)
- [KMA VilageFcstInfoService endpoint](https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0)
- [AirKorea realtime station measurement endpoint](https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty)
- [playbook.md](playbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown weather summaries, JSON API responses, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured data.go.kr API key and KMA grid coordinates; morning briefing output can combine weather and air-quality values.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
