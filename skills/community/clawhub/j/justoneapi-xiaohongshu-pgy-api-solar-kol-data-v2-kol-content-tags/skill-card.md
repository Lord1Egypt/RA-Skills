## Description:

Call GET /api/xiaohongshu-pgy/api/solar/kol/dataV2/kolContentTags/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Content Tags through JustOneAPI with userId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Xiaohongshu Creator Marketplace creator content tag data through JustOneAPI for creator evaluation, campaign planning, and benchmarking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a JustOneAPI token that may be exposed through command arguments or URL query strings.

Mitigation: Use narrowly scoped or short-lived tokens when available, avoid shared machines and verbose command logging, and rotate the token if it may have appeared in process telemetry or URL logs.

Risk: The security verdict is suspicious because token handling can expose sensitive account access or paid quota.

Mitigation: Review before installing when the token has broad access, paid quota, or sensitive account permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-api-solar-kol-data-v2-kol-content-tags)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v2_kol_content_tags&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v2_kol_content_tags&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON from the API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a userId query parameter.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
