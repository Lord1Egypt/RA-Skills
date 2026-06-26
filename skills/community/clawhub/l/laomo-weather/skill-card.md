## Description: <br>
Weather provides current weather, forecasts, air quality, pollen levels, weather alerts, lifestyle suggestions, and multi-city comparisons with Chinese and English output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrzhangkris](https://clawhub.ai/user/mrzhangkris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check current and forecast weather, compare cities, and request weather-related air quality, pollen, alert, and lifestyle guidance for travel or daily planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried locations are sent to external weather and geocoding providers. <br>
Mitigation: Use city-level locations instead of exact home or work coordinates when location privacy matters. <br>
Risk: Weather, air quality, pollen, and alert data can be unavailable, delayed, or inaccurate for some locations. <br>
Mitigation: Treat outputs as planning guidance and verify high-impact decisions with authoritative local weather or emergency sources. <br>


## Reference(s): <br>
- [ClawHub Weather Release](https://clawhub.ai/mrzhangkris/laomo-weather) <br>
- [wttr.in Help](https://wttr.in/:help) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1) <br>
- [Open-Meteo Air Quality API](https://air-quality-api.open-meteo.com/v1/air-quality) <br>
- [Open-Meteo Pollen API](https://pollen-api.open-meteo.com/v1/pollen) <br>
- [Open-Meteo Geocoding API](https://geocoding.open-meteo.com/v1/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Plain text, table text, or JSON weather reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese and English output; may include current conditions, forecasts, AQI, pollen, alerts, comparisons, and lifestyle suggestions.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
