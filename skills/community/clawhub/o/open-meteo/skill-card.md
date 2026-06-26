## Description: <br>
Gets current, hourly, and 7-day forecasts from Open-Meteo and can generate an interactive Weather Strip HTML/SVG widget for weather summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dapkus](https://clawhub.ai/user/dapkus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to answer weather questions, retrieve Open-Meteo forecast data, and generate a daily digest weather visualization for one or more locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Open-Meteo to fetch weather and geocoding data. <br>
Mitigation: Use it only when external requests to Open-Meteo are acceptable for the location data being queried. <br>
Risk: The weather-strip generator can write a local HTML file. <br>
Mitigation: Confirm the output path before writing and avoid overwriting unrelated files. <br>
Risk: Untrusted schedule or city names may be embedded into generated HTML. <br>
Mitigation: Use trusted schedule data or review generated HTML before embedding it in another page. <br>


## Reference(s): <br>
- [Open-Meteo Forecast API endpoint](https://api.open-meteo.com/v1/forecast) <br>
- [Open-Meteo Geocoding API endpoint](https://geocoding-api.open-meteo.com/v1/search?name=CityName&count=1) <br>
- [ClawHub skill page](https://clawhub.ai/dapkus/open-meteo) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; bundled scripts produce JSON forecast data or HTML/SVG weather widgets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses latitude, longitude, forecast mode, day count, unit selection, optional multi-city schedule JSON, and optional output file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
