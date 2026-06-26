## Description: <br>
Looks up current weather, 7-day forecasts, 24-hour hourly conditions, air quality, lifestyle indexes, and supported cities through JisuAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer weather questions for Chinese cities or supported location identifiers, then summarize JisuAPI weather JSON into user-facing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries may disclose location data to JisuAPI, especially when using exact coordinates or IP address. <br>
Mitigation: Prefer city-name queries where possible and avoid exact coordinates or IP address unless the user specifically needs that lookup. <br>
Risk: The skill depends on a JisuAPI key and the provider's quota, permissions, and availability. <br>
Mitigation: Use a dedicated JISU_API_KEY with normal quota controls and handle API errors or quota failures in the agent response. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/jisu-weather) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [JisuAPI Weather API](https://www.jisuapi.com/api/weather/) <br>
- [JisuAPI weather query endpoint](https://api.jisuapi.com/weather/query) <br>
- [JisuAPI weather city endpoint](https://api.jisuapi.com/weather/city) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from the weather helper script, typically summarized by the agent as Markdown or plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; weather lookups may use city, cityid, citycode, latitude/longitude, IP address, or a city-list command.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
