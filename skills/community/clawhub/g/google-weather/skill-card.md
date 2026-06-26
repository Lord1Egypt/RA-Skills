## Description: <br>
Google Weather API - accurate, real-time weather data. Get current conditions, temperature, humidity, wind, and forecasts. Powered by Google's Weather API for reliable, hyperlocal data updated every 15 minutes. Supports any location worldwide. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shaharsha](https://clawhub.ai/user/Shaharsha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve current weather, hourly forecasts, and raw weather JSON for locations worldwide through Google Weather and Geocoding services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requested location queries to Google Weather and Geocoding services. <br>
Mitigation: Use only when that data sharing is acceptable for the agent workflow and user context. <br>
Risk: The skill requires a Google API key for weather and geocoding requests. <br>
Mitigation: Use a scoped API key restricted to the required Google APIs and expected usage limits. <br>


## Reference(s): <br>
- [ClawHub Google Weather Skill Page](https://clawhub.ai/Shaharsha/google-weather) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>
- [Google Weather API](https://console.cloud.google.com/apis/library/weather.googleapis.com) <br>
- [Google Geocoding API](https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON] <br>
**Output Format:** [Plain text or JSON weather results, with markdown-style emphasis in formatted summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Google API key; supports metric or imperial units through GOOGLE_WEATHER_UNITS.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
