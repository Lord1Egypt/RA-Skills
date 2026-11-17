## Description:

查询实时天气、7 天预报、24 小时逐时、空气质量与生活指数，可查城市列表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to query JisuAPI weather data by city, city ID, city code, coordinates, or IP address, then summarize current conditions, forecasts, AQI, hourly weather, and lifestyle indexes for end users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the configured JISU_API_KEY and user-provided city, IP address, or latitude/longitude to JisuAPI.

Mitigation: Use city-level lookup unless IP-based or precise-coordinate weather results are intentionally needed, and only install the skill if sharing those inputs with JisuAPI is acceptable.

Risk: Weather calls depend on the external JisuAPI service, account permissions, and request quota.

Mitigation: Configure a valid JisuAPI AppKey, monitor provider quota or permission errors, and handle returned API error JSON before presenting results to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/jisu-weather)
- [JisuAPI home page](https://www.jisuapi.com/)
- [JisuAPI weather API documentation](https://www.jisuapi.com/api/weather/)
- [JisuAPI weather query endpoint](https://api.jisuapi.com/weather/query)
- [JisuAPI weather city endpoint](https://api.jisuapi.com/weather/city)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the JISU_API_KEY environment variable; weather lookups return provider JSON that agents may summarize into natural language.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
