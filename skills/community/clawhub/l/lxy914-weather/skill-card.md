## Description:

和风天气 API 查询服务，支持实时天气、天气预报和小时预报。使用城市名称进行查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxy914](https://clawhub.ai/user/lxy914)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to query QWeather for current weather, daily forecasts, and hourly forecasts by city name or location ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured QWEATHER_BASE_URL receives the API key and city or location queries.

Mitigation: Store QWEATHER_API_KEY as a secret environment variable and set QWEATHER_BASE_URL only to the official HTTPS QWeather host for the account.

## Reference(s):

- [QWeather Developer Portal](https://dev.qweather.com/)
- [ClawHub Skill Release](https://clawhub.ai/lxy914/skills/lxy914-weather)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration guidance]

**Output Format:** [Plain text or JSON from a Python command-line helper, with Markdown usage examples in the skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QWEATHER_API_KEY and QWEATHER_BASE_URL environment variables.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
