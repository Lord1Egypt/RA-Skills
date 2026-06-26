## Description: <br>
查询城市天气情况。使用场景：用户询问某个城市的天气、温度、或天气预报时。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gooduone](https://clawhub.ai/user/gooduone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Chinese-language weather questions for a named city, including current conditions, temperature, rainfall checks, and short forecasts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups may send city or location text to wttr.in. <br>
Mitigation: Avoid including sensitive personal details in weather queries and use HTTPS wttr.in URLs where possible. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/gooduone/gooduone-weather) <br>
- [wttr.in weather service](https://wttr.in) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline curl commands; weather responses may be plain text, concise text, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Chinese-language output with lang=zh, concise one-line output with format=3, and JSON output with format=j1.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
