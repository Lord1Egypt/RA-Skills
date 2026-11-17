## Description:

Provides real-time Hong Kong weather, warnings, and 9-day forecasts from the Hong Kong Observatory official open data API in Traditional Chinese or English, with no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mic007p](https://clawhub.ai/user/mic007p)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Hong Kong-specific weather questions, including current conditions, active weather warnings, rainfall, UV index, and 9-day forecasts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live network requests to data.weather.gov.hk, so answers can fail or be unavailable if the Hong Kong Observatory API or network access is unavailable.

Mitigation: Restrict network access to the documented HKO domain and surface the exact API error instead of fabricating weather data.

Risk: The skill may answer in Traditional Chinese when the user's language preference is unclear.

Mitigation: Use the user's query language when clear, or ask for the preferred language before returning weather details.

## Reference(s):

- [Hong Kong Weather Skill Page](https://clawhub.ai/mic007p/skills/hk-weather)
- [Hong Kong Observatory Open Data API](https://data.weather.gov.hk/weatherAPI/opendata/weather.php)
- [Publisher Profile](https://clawhub.ai/user/mic007p)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text or Markdown response based on live weather data returned by the skill script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Traditional Chinese and English; typical response time is 2-5 seconds.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
