## Description:

查询指定城市的实时天气、近 5 天预报和生活指数，并通过聚合数据 juhe.cn API 返回温度、湿度、AQI、天气状况、风向等信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent builders use this skill to answer city weather questions in Chinese, including current conditions, near-term forecasts, and life-index guidance such as clothing, sport, car wash, and UV suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the API key and city query over unencrypted HTTP.

Mitigation: Use a low-privilege or disposable API key, avoid sensitive production credentials, and change endpoints to HTTPS before production use if Juhe supports HTTPS for these API paths.

Risk: City names queried through the script may be visible to network observers and are sent to Juhe.

Mitigation: Avoid submitting sensitive location queries and disclose that weather lookups are sent to the third-party Juhe service.

Risk: Providing the API key through scripts/.env or the --key argument can increase accidental credential exposure.

Mitigation: Prefer the JUHE_WEATHER_KEY environment variable and avoid logging commands or files that contain credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-weather)
- [Publisher profile](https://clawhub.ai/user/juhemcp)
- [Juhe Weather API documentation](https://www.juhe.cn/docs/api/id/73)
- [Juhe platform](https://www.juhe.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text and JSON from the weather script, with Markdown usage guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JUHE_WEATHER_KEY API credential; supports city weather queries and optional life-index output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
