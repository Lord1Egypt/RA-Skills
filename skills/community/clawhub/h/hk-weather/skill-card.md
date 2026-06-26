## Description: <br>
Fetches current Hong Kong weather, warnings, rainfall, UV index, and forecasts from the Hong Kong Observatory official open data API with Traditional Chinese and English output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mic007p](https://clawhub.ai/user/mic007p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Hong Kong-specific weather questions with current conditions, warnings, rainfall, UV index, and forecasts from HKO open data in Traditional Chinese or English. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent runs python3 locally and makes outbound HTTPS requests for public weather data. <br>
Mitigation: Limit execution to the documented hk_weather.py commands and the data.weather.gov.hk open-data endpoint; no credentials are required. <br>
Risk: Weather responses can be unavailable or incomplete if the HKO API request fails. <br>
Mitigation: Use the script's returned error as the response basis and avoid fabricating weather data. <br>


## Reference(s): <br>
- [ClawHub Hong Kong Weather Skill](https://clawhub.ai/mic007p/hk-weather) <br>
- [Hong Kong Observatory Open Data API](https://data.weather.gov.hk/weatherAPI/opendata/weather.php) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text weather reports with concise agent-facing guidance and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports current, warning, forecast, and all modes with tc or en language selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
