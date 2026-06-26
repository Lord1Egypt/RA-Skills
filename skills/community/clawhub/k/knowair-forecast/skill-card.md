## Description: <br>
Get hourly and daily weather forecasts by latitude and longitude through the Caiyun Weather API, including temperature, precipitation, wind, humidity, weather conditions, and life-index details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuowang-ai](https://clawhub.ai/user/shuowang-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve short-range hourly forecasts and up to 15-day daily forecasts for a coordinate-based location, then present the results as concise weather guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided longitude and latitude coordinates to Caiyun for weather lookups. <br>
Mitigation: Use approximate coordinates when exact private locations are not required. <br>
Risk: The skill requires a Caiyun API token for forecast requests. <br>
Mitigation: Use a dedicated token where possible and avoid exposing it in prompts, logs, or shared command output. <br>
Risk: Forecast retrieval depends on internet access and Caiyun API availability. <br>
Mitigation: Check connectivity and API errors before relying on the forecast output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuowang-ai/knowair-forecast) <br>
- [Publisher profile](https://clawhub.ai/user/shuowang-ai) <br>
- [Caiyun Weather API endpoint](https://api.caiyunapp.com/v2.6) <br>
- [Usage examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown forecast summaries with shell command examples; the bundled script returns JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, internet access, a Caiyun API token, and longitude/latitude coordinates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
