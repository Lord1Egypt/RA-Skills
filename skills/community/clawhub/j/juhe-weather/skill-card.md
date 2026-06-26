## Description: <br>
Queries Juhe weather data for a specified city, including current conditions, a five-day forecast, AQI, wind, humidity, and lifestyle indices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to answer weather questions for Chinese cities and to retrieve lifestyle index guidance such as clothing, sport, car wash, and UV recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Juhe API key can be exposed if it is passed on the command line or committed in scripts/.env. <br>
Mitigation: Prefer the JUHE_WEATHER_KEY environment variable, avoid shell history exposure, and keep local .env files out of version control. <br>
Risk: The bundled script uses HTTP Juhe API endpoints for live weather requests. <br>
Mitigation: Use HTTPS endpoints if Juhe supports them in the deployment environment, and avoid sending sensitive credentials over untrusted networks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/juhe-weather) <br>
- [Juhe Weather API documentation](https://www.juhe.cn/docs/api/id/73) <br>
- [Juhe API platform](https://www.juhe.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text with command examples and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JUHE_WEATHER_KEY API key for live lookups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
