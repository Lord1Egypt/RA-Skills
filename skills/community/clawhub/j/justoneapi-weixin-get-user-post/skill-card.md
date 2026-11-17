## Description:

Call GET /api/weixin/get-user-post/v1 for WeChat Official Accounts User Published Posts through JustOneAPI with wxid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve published-post data for a WeChat Official Account by wxid through JustOneAPI, supporting account monitoring workflows that need titles, publish times, and summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through chat, logs, shell history, process listings, or URL query logging because this helper accepts it on the command line and sends it as a query parameter.

Mitigation: Use a narrowly scoped, revocable token, avoid pasting token values into chat or logs, and rotate the token if command or request logs may have captured it.

Risk: The skill sends the supplied wxid lookup to JustOneAPI, so users must trust that service with the account lookup request.

Mitigation: Install and run the skill only when JustOneAPI is an acceptable third-party service for the intended lookup.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_user_post&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_user_post&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-weixin-get-user-post)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Markdown summary followed by raw JSON from the API helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the JUST_ONE_API_TOKEN environment variable and a wxid query parameter.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
