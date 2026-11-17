## Description:

Hong Kong weather information for current conditions, forecasts, rainfall, warnings, alerts, and one-minute average temperature using Hong Kong Observatory public data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenho1394](https://clawhub.ai/user/stevenho1394)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer Hong Kong weather questions with current conditions, local forecasts, warnings, rainfall, humidity, and regional temperature context. It supports English, Traditional Chinese, and Simplified Chinese responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to Hong Kong Observatory weather endpoints.

Mitigation: Install only where public weather endpoint access is acceptable and review network access expectations before deployment.

Risk: The bundled helper script writes a small local cache in the user's home directory.

Mitigation: Review cache behavior and remove or restrict the cache directory if local persistence is not acceptable.

Risk: Default output is Traditional Chinese, which may surprise users expecting English.

Mitigation: Set the language option explicitly when English or Simplified Chinese output is required.

## Reference(s):

- [HKO OpenData Weather API](https://data.weather.gov.hk/weatherAPI/opendata/weather.php)
- [HKO Latest 1-Minute Temperature CSV](https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/latest_1min_temperature.csv)
- [HKO 1-Minute Temperature CSV Reference](references/1min-temp-csv.md)
- [ClawHub Skill Page](https://clawhub.ai/stevenho1394/skills/hk-weather-info)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text weather summaries with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current weather, forecast text, warnings, update times, regional station matches, and one-minute average temperature.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
