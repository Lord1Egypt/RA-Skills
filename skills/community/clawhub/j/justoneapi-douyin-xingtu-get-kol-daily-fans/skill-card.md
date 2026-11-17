## Description:

Call GET /api/douyin-xingtu/get-kol-daily-fans/v1 for Douyin Creator Marketplace (Xingtu) Follower Growth Trend through JustOneAPI with endDate, kolId, and startDate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call a JustOneAPI Douyin Creator Marketplace endpoint that returns historical follower growth data for a specified KOL and date range. The data supports creator evaluation, campaign planning, and marketplace research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API token handling creates a meaningful credential exposure risk, including possible exposure through process listings or URL logs.

Mitigation: Use a narrowly scoped or short-lived JustOneAPI token when available, avoid pasting token values into chat or logs, and rotate the token if exposure is suspected.

Risk: The skill depends on a third-party JustOneAPI request path for Douyin/Xingtu data.

Mitigation: Review JustOneAPI terms, access permissions, and response payloads before relying on outputs in production workflows.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_daily_fans&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_daily_fans&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-kol-daily-fans)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; required endpoint inputs are kolId, startDate, and endDate.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
