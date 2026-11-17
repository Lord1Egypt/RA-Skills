## Description:

Call GET /api/douyin-xingtu/gw/api/data_sp/get_author_fans_distribution/v1 for Douyin Creator Marketplace (Xingtu) Follower Distribution through JustOneAPI with oAuthorId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to call JustOneAPI's Douyin Creator Marketplace (Xingtu) follower distribution endpoint for a creator identified by oAuthorId, supporting creator evaluation, campaign planning, and marketplace research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command arguments, URLs, process records, shell history, proxy logs, gateway logs, or server logs.

Mitigation: Use a narrowly scoped token where possible, avoid sharing command output or logs, and rotate the token if it may have been captured.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-data-sp-get-author-fans-distribution)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_fans_distribution&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_fans_distribution&utm_content=project_link)
- [Generated Operations Reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Markdown summary with endpoint details, executable helper command, and raw JSON response data when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and oAuthorId; authorType is optional and defaults to FAN.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
