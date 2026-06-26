## Description: <br>
Looks up current weather for a requested city or place, supporting Chinese, English, and pinyin input with Beijing as the default location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maomaoshuo](https://clawhub.ai/user/maomaoshuo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to answer current-weather questions for global cities and to summarize temperature, conditions, wind speed, wind direction, and update time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The city or place name requested by the user is sent to Open-Meteo for geocoding and weather lookup. <br>
Mitigation: Avoid submitting sensitive private locations when that disclosure would be inappropriate, and review outbound network policy before deployment. <br>
Risk: The skill runs a bundled Python helper and may require the requests package. <br>
Mitigation: Install dependencies in a controlled environment and review the helper script before enabling Bash execution. <br>
Risk: Geocoding can choose an unintended location when a city name is ambiguous. <br>
Mitigation: Use more specific city, region, or country names when location precision matters. <br>


## Reference(s): <br>
- [天气查询详细指南](references/weather_details.md) <br>
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text weather report with a concise summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes city, temperature, weather condition, wind speed, wind direction, day/night state, and update time when available.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
