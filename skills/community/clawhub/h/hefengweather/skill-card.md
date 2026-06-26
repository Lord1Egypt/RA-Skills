## Description: <br>
Provides QWeather-based weather lookup capabilities for current conditions, multi-day and hourly forecasts, air quality, lifestyle indices, weather warnings, astronomy data, minute-level precipitation, grid weather, and geographic search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengyucn](https://clawhub.ai/user/fengyucn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent answer weather, air quality, warning, astronomy, precipitation, grid-weather, and location-search questions through QWeather API-backed scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires QWeather API credentials, and saved credentials may be exposed if the local configuration file is not protected. <br>
Mitigation: Prefer environment variables or the --no-save option; if credentials are saved, keep ~/.config/qweather/.env owner-only. <br>
Risk: The configurable API host controls where weather API requests are sent. <br>
Mitigation: Verify HEFENG_API_HOST points to an official or intended QWeather API domain before running queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengyucn/hefengweather) <br>
- [QWeather developer platform](https://dev.qweather.com/) <br>
- [QWeather documentation](https://dev.qweather.com/docs/) <br>
- [QWeather API reference](https://dev.qweather.com/docs/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language weather summaries and optional JSON API responses produced from script output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QWeather API configuration through environment variables or an optional local configuration file.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
