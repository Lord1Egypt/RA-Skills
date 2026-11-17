## Description:

天气查询 - 即刻数据 lets an agent query current weather and 7-day or 15-day forecasts by province, city, and optional district using Jike API data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer weather questions for Chinese province, city, and optional district inputs. It supports current conditions plus 7-day and 15-day forecasts and can return either readable text or JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changing JIKE_API_BASE_URL can redirect requests and expose the Jike AppKey and queried location to an arbitrary endpoint.

Mitigation: Run with controlled environment variables, avoid setting JIKE_API_BASE_URL, and restrict outbound access to https://api.jikeapi.cn.

Risk: The Jike AppKey is included in request URLs and may appear in URL logs or debugging output.

Mitigation: Treat JIKE_WEATHER_QUERY_KEY and JIKE_APPKEY as secrets, avoid logging full request URLs, and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-weather-query)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Jike weather current conditions endpoint](https://api.jikeapi.cn/v1/weather/query/by-area)
- [Jike weather 7-day forecast endpoint](https://api.jikeapi.cn/v1/weather/query/7d)
- [Jike weather 15-day forecast endpoint](https://api.jikeapi.cn/v1/weather/query/15d)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text weather summary or JSON object, with documented shell command usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a Jike AppKey in JIKE_WEATHER_QUERY_KEY or JIKE_APPKEY; sends outbound requests to api.jikeapi.cn.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
