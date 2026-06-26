## Description: <br>
Get current weather and forecasts with no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars82311111](https://clawhub.ai/user/mars82311111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to ask an agent for quick current weather and forecast lookup commands for named locations, airport codes, or coordinates using public weather services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookup queries can disclose locations or coordinates to wttr.in or Open-Meteo. <br>
Mitigation: Use only the location granularity needed and avoid querying sensitive private locations. <br>
Risk: Some wttr.in examples omit an explicit HTTPS scheme. <br>
Mitigation: Prefer https://wttr.in URLs when running curl commands. <br>
Risk: Forecasts from public services may be unavailable, delayed, or inaccurate. <br>
Mitigation: Cross-check weather data before relying on it for operational or safety-sensitive decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mars82311111/marsai-weather-forecast) <br>
- [wttr.in Help](https://wttr.in/:help) <br>
- [Open-Meteo Forecast API Documentation](https://open-meteo.com/en/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and service URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
