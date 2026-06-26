## Description: <br>
Provides Hong Kong current weather, forecasts, warnings, rainfall, humidity, and 1-minute temperature information from Hong Kong Observatory public data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenho1394](https://clawhub.ai/user/stevenho1394) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer Hong Kong weather questions with HKO current conditions, local forecasts, warnings, regional filtering, and multilingual output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts HKO public weather endpoints and stores public weather responses in a local cache. <br>
Mitigation: Use it only where outbound access to HKO public data is acceptable, and review any request for secrets because this skill should not require API keys or sensitive credentials. <br>
Risk: Weather responses may be unavailable or stale if the external HKO service is unreachable or cached data is used. <br>
Mitigation: Check the displayed update time and treat weather output as advisory public data rather than a source for safety-critical decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevenho1394/hk-weather-info) <br>
- [HKO OpenData API](https://data.weather.gov.hk/weatherAPI/opendata/weather.php) <br>
- [HKO 1-Minute Temperature CSV reference](references/1min-temp-csv.md) <br>
- [Latest 1-minute temperature CSV](https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/latest_1min_temperature.csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style weather summary with optional CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports regional filtering, en/tc/sc language selection, public HKO API calls, and local caching of public weather responses.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
