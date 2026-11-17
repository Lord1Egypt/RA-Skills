## Description:

Get hourly and daily weather forecasts by latitude and longitude via the Caiyun Weather API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuowang-ai](https://clawhub.ai/user/shuowang-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve hourly or daily forecasts for specified coordinates and summarize temperature, precipitation, wind, humidity, and life-index details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forecast lookups send the requested coordinates and Caiyun API token to Caiyun's weather service.

Mitigation: Use the documented CAIYUN_TOKEN environment variable or token config file, and provide coarse coordinates when an exact location is unnecessary.

Risk: Precise coordinates may reveal sensitive location context.

Mitigation: Round or generalize coordinates before running the forecast query when precise location is not needed.

## Reference(s):

- [Usage examples](artifact/examples.md)
- [Caiyun Weather API endpoint](https://api.caiyunapp.com/v2.6)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON forecast output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, internet access, CAIYUN_TOKEN, and longitude/latitude inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
