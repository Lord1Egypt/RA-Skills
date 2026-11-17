## Description:

Provides air quality forecasts through the Caiyun Weather API, including AQI, pollutant values, trend summaries, best and worst forecast periods, and health-oriented activity guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuowang-ai](https://clawhub.ai/user/shuowang-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer air quality, pollution, AQI, PM2.5, and outdoor activity questions for a requested location. It is most useful when an agent needs structured forecast data plus a short user-facing interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the requested coordinates and a Caiyun API token to Caiyun services.

Mitigation: Use it only when sharing those coordinates with Caiyun is acceptable, and prefer the CAIYUN_TOKEN environment variable over a local token file when possible.

Risk: Health and exercise recommendations are air-quality guidance and may not account for individual medical needs.

Mitigation: Present recommendations as general guidance and avoid treating them as medical advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuowang-ai/skills/knowair-weather)
- [Caiyun Weather API endpoint](https://api.caiyunapp.com/v2.6)
- [Caiyun station AQI forecast endpoint](https://singer.caiyunhub.com/v3/aqi/forecast/station)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and summarized JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current AQI level, pollutant values, trend summaries, best and worst periods, station fallback details, and exercise recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
