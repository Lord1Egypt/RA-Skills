## Description: <br>
查询甘肃省泾川县7天天气预报，包含天气状况、温度、降雨概率、日出日落时间和出行建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ltap266](https://clawhub.ai/user/ltap266) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Jingchuan County weather requests with a 7-day forecast, sunrise and sunset times, and short travel guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forecast data may be inaccurate or tampered with on untrusted networks because the script disables HTTPS certificate validation and falls back to HTTP. <br>
Mitigation: Use normal HTTPS certificate validation, remove HTTP fallback, and confirm the Open-Meteo response before relying on the forecast in safety-sensitive decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ltap266/jingchuan-weather) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style weather forecast table with concise travel guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches a 7-day forecast for fixed Jingchuan County coordinates from Open-Meteo.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
