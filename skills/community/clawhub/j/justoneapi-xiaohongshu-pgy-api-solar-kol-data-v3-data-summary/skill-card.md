## Description:

Call GET /api/xiaohongshu-pgy/api/solar/kol/dataV3/dataSummary/v1 for Xiaohongshu Creator Marketplace (Pugongying) Data Summary through JustOneAPI with userId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to call JustOneAPI for Xiaohongshu Creator Marketplace creator summary data by userId, supporting creator evaluation, campaign planning, and benchmarking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens can be exposed through command lines, logs, or URL query strings.

Mitigation: Use a narrowly scoped or short-lived JustOneAPI token when available, avoid logging commands or full request URLs, and rotate the token if exposure is suspected.

Risk: The release has a suspicious security verdict from ClawHub scan evidence.

Mitigation: Review the skill before installing, especially when the token has billing or broad account access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-api-solar-kol-data-v3-data-summary)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v3_data_summary&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v3_data_summary&utm_content=project_link)
- [Generated operation reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses operation apiSolarKolDataV3DataSummaryV1 with required userId, required JUST_ONE_API_TOKEN, and optional business query value.]

## Skill Version(s):

1.0.0 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
