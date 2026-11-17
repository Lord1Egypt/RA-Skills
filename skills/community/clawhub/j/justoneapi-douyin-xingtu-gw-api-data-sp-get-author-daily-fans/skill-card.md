## Description:

Call GET /api/douyin-xingtu/gw/api/data_sp/get_author_daily_fans/v1 for Douyin Creator Marketplace (Xingtu) Follower Growth Trend through JustOneAPI with endDate, oAuthorId, and startDate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call a JustOneAPI endpoint for Douyin Creator Marketplace follower growth trend data. The output supports creator evaluation, campaign planning, and marketplace research over a requested author and date range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may appear in process metadata and request URLs because this release passes the token through command-line arguments and query parameters.

Mitigation: Use short-lived tokens, avoid logging full command lines or URLs, and rotate the token if logs may have captured it.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_daily_fans&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_daily_fans&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-data-sp-get-author-daily-fans)
- [Generated Operations Reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown summary with raw JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and endpoint parameters oAuthorId, startDate, and endDate.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
