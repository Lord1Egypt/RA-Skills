## Description:

Get hourly and daily weather forecasts by latitude and longitude via the Caiyun Weather API, including temperature trends, weather conditions, precipitation probability, wind, humidity, air quality, and life indices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuowang-ai](https://clawhub.ai/user/shuowang-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve location-based hourly or daily weather forecasts and summarize conditions, precipitation, air quality, and life-index signals for planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forecast requests send requested coordinates to Caiyun Weather, which may reveal a precise location.

Mitigation: Use approximate coordinates when exact private locations are not necessary.

Risk: The skill requires a Caiyun API token for forecast queries.

Mitigation: Store the token in the CAIYUN_TOKEN environment variable when possible and avoid exposing it in shared prompts, logs, or command output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuowang-ai/skills/knowair-air-quality)
- [Publisher profile](https://clawhub.ai/user/shuowang-ai)
- [Caiyun Weather API endpoint](https://api.caiyunapp.com/v2.6)
- [Usage examples](examples.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON from the helper script, typically summarized by the agent as concise Markdown or text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports English and Chinese output, hourly forecasts up to 360 hours, daily forecasts up to 15 days, and configurable detail levels.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
