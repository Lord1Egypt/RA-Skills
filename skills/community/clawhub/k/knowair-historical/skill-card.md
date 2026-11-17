## Description:

Get historical weather data up to 72 hours back via the Caiyun Weather API, including temperature, weather conditions, precipitation, wind, humidity, apparent temperature, and air quality at regular intervals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuowang-ai](https://clawhub.ai/user/shuowang-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer questions about recent past weather for a coordinate pair, including yesterday's weather, earlier temperatures, and weather history over the last 1 to 72 hours.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requested longitude and latitude coordinates to Caiyun's API.

Mitigation: Avoid using the skill for locations considered sensitive, and only submit coordinates you are comfortable sharing with Caiyun.

Risk: The skill requires a Caiyun API token.

Mitigation: Provide the token through CAIYUN_TOKEN or a dedicated ~/.config/knowair/token file, and avoid exposing it in prompts, logs, or shared command output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuowang-ai/skills/knowair-historical)
- [Caiyun Weather API endpoint](https://api.caiyunapp.com/v2.6)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON weather results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, internet access, CAIYUN_TOKEN, longitude, latitude, and an optional 1 to 72 hour lookback window.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
