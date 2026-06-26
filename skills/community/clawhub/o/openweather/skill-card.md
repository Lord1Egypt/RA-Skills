## Description: <br>
Get current weather, hourly forecasts, and 8-day daily forecasts for any location worldwide using OpenWeather One Call API 3.0. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joshua-ensley](https://clawhub.ai/user/joshua-ensley) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent answer weather, temperature, precipitation, and forecast questions for a city or configured default location. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OpenWeather API key and makes outbound requests for weather lookups. <br>
Mitigation: Provide the key through declared environment configuration only, confirm One Call 3.0 is enabled, and allow network access only to expected OpenWeather endpoints. <br>
Risk: Weather lookups can consume OpenWeather quota or paid API calls. <br>
Mitigation: Review OpenWeather account limits before deployment and monitor usage for agents that may issue repeated forecast requests. <br>


## Reference(s): <br>
- [OpenWeather Skill Page](https://clawhub.ai/joshua-ensley/openweather) <br>
- [OpenWeather One Call API 3.0 Quick Reference](api-reference.md) <br>
- [OpenWeather API](https://openweathermap.org/api) <br>
- [OpenWeather One Call endpoint](https://api.openweathermap.org/data/3.0/onecall) <br>
- [OpenWeather Geocoding endpoint](https://api.openweathermap.org/geo/1.0/direct) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Human-readable CLI text for current, hourly, and daily weather forecasts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENWEATHER_API_KEY; optional OPENWEATHER_UNITS and OPENWEATHER_DEFAULT_LOCATION control units and default lookup location.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
