## Description: <br>
Get current weather data, forecasts, and weather information from OpenWeatherMap API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[philiplawlor](https://clawhub.ai/user/philiplawlor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve and present current weather and forecast information for a location through the OpenWeatherMap API. It supports city-name and coordinate queries with metric, imperial, or standard units. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries may disclose requested locations to OpenWeatherMap. <br>
Mitigation: Prefer city-level queries over precise coordinates when possible. <br>
Risk: An OpenWeatherMap API key can be exposed if copied into prompts, shell history, or shared files. <br>
Mitigation: Use a dedicated API key stored in OPENWEATHERMAP_API_KEY or ~/.openweathermap and rotate it if exposed. <br>
Risk: Some forecast capabilities, including One Call API 3.0 hourly, daily, minutely forecasts, and alerts, may require a paid subscription. <br>
Mitigation: Confirm the active OpenWeatherMap plan before relying on paid-only forecast features. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/philiplawlor/openweathermap) <br>
- [Publisher Profile](https://clawhub.ai/user/philiplawlor) <br>
- [OpenWeatherMap API Keys](https://home.openweathermap.org/api_keys) <br>
- [OpenWeatherMap Current Weather Endpoint](https://api.openweathermap.org/data/2.5/weather) <br>
- [OpenWeatherMap Forecast Endpoint](https://api.openweathermap.org/data/2.5/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with API request examples and formatted weather summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENWEATHERMAP_API_KEY or a ~/.openweathermap API key file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
