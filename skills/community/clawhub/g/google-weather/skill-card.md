## Description:

Google Weather API - accurate, real-time weather data. Get current conditions, temperature, humidity, wind, and forecasts. Powered by Google's Weather API for reliable, hyperlocal data updated every 15 minutes. Supports any location worldwide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaharsha](https://clawhub.ai/user/shaharsha)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve current weather, hourly forecasts, and raw weather JSON for locations worldwide through Google's Weather and Geocoding APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requested locations to Google for geocoding and weather lookup.

Mitigation: Use it only where sharing queried locations with Google is acceptable.

Risk: The skill requires a Google API key that may have billing and access implications.

Mitigation: Restrict the API key and configure billing controls in Google Cloud before use.

## Reference(s):

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Weather API](https://console.cloud.google.com/apis/library/weather.googleapis.com)
- [Google Geocoding API](https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com)
- [Google Weather on ClawHub](https://clawhub.ai/shaharsha/skills/google-weather)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown text summaries, JSON data, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports metric or imperial units through GOOGLE_WEATHER_UNITS; requires a Google API key.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
