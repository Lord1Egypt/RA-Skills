## Description:

Fetches Hong Kong Observatory weather data, forecasts, and warning signals and formats weather updates for OpenClaw and Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[firenai3424](https://clawhub.ai/user/firenai3424)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to retrieve Hong Kong weather conditions, forecasts, and warning signals, with Traditional Chinese output suitable for Discord weather updates.

### Deployment Geography for Use:

Global; weather coverage is Hong Kong.

## Known Risks and Mitigations:

Risk: Optional Discord posting, cron jobs, and auto-refresh settings can send weather messages externally on a schedule.

Mitigation: Review the Discord channel, auto_post setting, cron entries, and refresh interval before enabling scheduled posting.

Risk: HKO weather data is subject to separate attribution, disclaimer, and non-commercial-use terms described in the artifacts.

Mitigation: Keep HKO attribution and disclaimer text in displayed outputs and confirm intended use against HKO terms before using the data commercially.

## Reference(s):

- [HKO Weather Skill on ClawHub](https://clawhub.ai/firenai3424/skills/hko-weather)
- [HKO Open Data Portal](https://www.hko.gov.hk/tc/abouthko/opendata_intro.htm)
- [HKO Open Data API Documentation](https://www.hko.gov.hk/tc/weatherAPI/doc/files/HKO_Open_Data_API_Documentation.pdf)
- [DATA.GOV.HK HKO Datasets](https://data.gov.hk/tc-datasets/provider/hk-hko)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown weather reports, JSON API responses, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Traditional Chinese and English weather output; optional Discord posting and scheduled refresh configuration]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
