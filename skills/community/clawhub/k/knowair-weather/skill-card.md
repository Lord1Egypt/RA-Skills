## Description: <br>
Get comprehensive air quality forecast from monitoring stations with up to 15-day coverage via the Caiyun Weather API, including AQI, PM2.5, PM10, O3, NO2, SO2, CO values, trends, best and worst periods, and health recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuowang-ai](https://clawhub.ai/user/shuowang-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve current and forecast air-quality conditions for a requested location, then present pollutant trends, best or worst periods, and practical health guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Caiyun Weather API token that may be exposed if stored or logged carelessly. <br>
Mitigation: Use a service-specific token, keep local token files protected, and avoid pasting credentials into prompts or shared logs. <br>
Risk: Queried coordinates are sent to Caiyun to fetch AQI forecasts. <br>
Mitigation: Use approximate coordinates when precise location is not necessary and disclose that location coordinates are shared with Caiyun. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shuowang-ai/knowair-weather) <br>
- [Caiyun Weather API](https://api.caiyunapp.com/v2.6) <br>
- [Caiyun AQI Station Forecast API](https://singer.caiyunhub.com/v3/aqi/forecast/station) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summary with optional bash command examples and structured air-quality readings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Caiyun Weather API token, longitude and latitude coordinates, and internet access; supports English or Chinese output and configurable forecast duration/detail.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
