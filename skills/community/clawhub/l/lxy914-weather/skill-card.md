## Description: <br>
和风天气 API 查询服务，支持实时天气、天气预报和小时预报。使用城市名称进行查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxy914](https://clawhub.ai/user/lxy914) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query QWeather for current conditions, daily forecasts, and hourly forecasts by city name or location ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured weather API host receives the QWeather API key with each request. <br>
Mitigation: Use the official QWeather API host for the account and keep QWEATHER_API_KEY private. <br>
Risk: Weather output may be delayed or constrained by service quota. <br>
Mitigation: Account for the documented 5-20 minute real-time data delay and monitor QWeather request limits before relying on repeated queries. <br>


## Reference(s): <br>
- [QWeather Developer Portal](https://dev.qweather.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/lxy914/lxy914-weather) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON weather results with Markdown usage guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QWEATHER_API_KEY and QWEATHER_BASE_URL environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
