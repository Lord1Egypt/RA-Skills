## Description: <br>
Provides real-time weather and air quality index data for any location using Open-Meteo and WAQI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guchigangz](https://clawhub.ai/user/guchigangz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to retrieve current weather and AQI for a named location, with either human-readable text or JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location queries are sent to Open-Meteo and WAQI. <br>
Mitigation: Use only for locations acceptable to share with those external services. <br>
Risk: AQI retrieval requires a WAQI API token. <br>
Mitigation: Use a dedicated WAQI token and avoid exposing it in prompts, logs, or shared output. <br>
Risk: The artifact claims VirusTotal clean, but the server security evidence says the supplied VT status is pending. <br>
Mitigation: Rely on the server security verdict and rescan before deployment if current malware status is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guchigangz/hb-weather-aqi) <br>
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>
- [World Air Quality Index API](https://api.waqi.info/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Plain text summary or formatted JSON string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a location input and optional JSON output mode; AQI requests use the WAQITOKEN environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
