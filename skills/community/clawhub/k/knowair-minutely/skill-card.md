## Description:

Gets minute-level precipitation forecasts for the next 2 hours via the Caiyun Weather API, including precipitation intensity samples and 30-minute probability data for supported locations, primarily major Chinese cities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuowang-ai](https://clawhub.ai/user/shuowang-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer imminent rain, precipitation, and umbrella-planning questions for supported China locations when longitude and latitude are available.

### Deployment Geography for Use:

Global; forecast coverage is mainly for supported locations in China.

## Known Risks and Mitigations:

Risk: The skill requires a Caiyun Weather API token and sends queried longitude/latitude coordinates to Caiyun.

Mitigation: Use the CAIYUN_TOKEN environment variable, avoid sensitive locations when inappropriate, and invoke the skill only for supported weather lookups.

Risk: Minutely precipitation data may be unavailable or less useful outside supported China coverage areas.

Mitigation: Tell users when data is unavailable and avoid presenting unsupported forecasts as definitive.

## Reference(s):

- [KnowAir Minutely ClawHub release](https://clawhub.ai/shuowang-ai/skills/knowair-minutely)
- [Caiyun Weather API endpoint](https://api.caiyunapp.com/v2.6)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Caiyun's natural-language description, five-minute precipitation intensity samples, datasource, and 30-minute probability periods.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
