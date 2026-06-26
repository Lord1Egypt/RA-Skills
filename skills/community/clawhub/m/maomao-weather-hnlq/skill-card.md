## Description: <br>
Queries current weather for global cities, supporting Chinese, English, and pinyin city input with automatic best-match location handling and a Beijing default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaodiyaochaoshen2](https://clawhub.ai/user/xiaodiyaochaoshen2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up current weather conditions for a named city and summarize temperature, weather condition, wind speed, wind direction, daytime status, and update time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries may disclose the requested city name to Open-Meteo services. <br>
Mitigation: Invoke the skill only for explicit weather lookups where sharing the city name with the weather API is acceptable. <br>
Risk: Current weather data may be delayed or city matching may choose an unintended location when names are ambiguous. <br>
Mitigation: Use specific city names, country suffixes, or pinyin/English variants and treat results as current-weather guidance rather than a forecast or safety-critical source. <br>


## Reference(s): <br>
- [Weather Details](references/weather_details.md) <br>
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search) <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaodiyaochaoshen2/maomao-weather-hnlq) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Formatted plain text weather report with a concise summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Current weather only; city names may be sent to Open-Meteo APIs during lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
