## Description: <br>
根据省份、城市、区县查询当前天气实况、未来7天和未来15天天气预报，数据由即刻数据开放接口提供。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer weather questions for Chinese province, city, and district names, including current conditions and 7-day or 15-day forecasts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookup locations and the JikeAPI AppKey are sent to the documented JikeAPI weather service. <br>
Mitigation: Use the skill only when this data sharing is acceptable, and avoid querying locations more specific than needed. <br>
Risk: The JIKE_API_BASE_URL override can redirect requests to a different endpoint. <br>
Mitigation: Set JIKE_API_BASE_URL only when the alternate endpoint is intentionally trusted. <br>
Risk: Command traces or logs can expose full request URLs that include the AppKey. <br>
Mitigation: Do not share logs, shell history, or debug output that contains request URLs or credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-weather-query) <br>
- [JikeAPI homepage](https://www.jikeapi.cn/) <br>
- [JikeAPI weather query endpoint](https://api.jikeapi.cn/v1/weather/query/by-area) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Plain text weather summaries, tabular forecast text, or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JIKE_WEATHER_QUERY_KEY or JIKE_APPKEY credential.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
