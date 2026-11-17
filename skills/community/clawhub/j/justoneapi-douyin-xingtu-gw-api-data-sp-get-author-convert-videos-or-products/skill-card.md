## Description:

Call GET /api/douyin-xingtu/gw/api/data_sp/get_author_convert_videos_or_products/v1 for Douyin Creator Marketplace (Xingtu) Conversion Resources through JustOneAPI with oAuthorId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call a focused JustOneAPI endpoint for Douyin Xingtu creator conversion resources. It supports commerce analysis and campaign optimization by retrieving video or product conversion data for a supplied creator author ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required JustOneAPI token may be exposed through command arguments or URL logs.

Mitigation: Use a narrowly scoped or disposable token where possible, avoid pasting token values into chat or logs, and review local process telemetry and server-side logging exposure before installation.

Risk: The skill sends authenticated requests to a third-party API wrapper.

Mitigation: Review the skill before installing when the token has broad scope or paid quota, and confirm that the endpoint and parameters match the intended Douyin Xingtu lookup.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-data-sp-get-author-convert-videos-or-products)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_convert_videos_or_products&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_convert_videos_or_products&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Endpoint-specific summary followed by raw JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and oAuthorId; optional query filters include platform, industryId, range, detailType, and page.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
