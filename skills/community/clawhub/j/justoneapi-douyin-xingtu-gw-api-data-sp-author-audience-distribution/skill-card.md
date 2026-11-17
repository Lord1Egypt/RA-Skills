## Description:

Call GET /api/douyin-xingtu/gw/api/data_sp/author_audience_distribution/v1 for Douyin Creator Marketplace (Xingtu) Audience Distribution through JustOneAPI with oAuthorId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external API users use this skill to call JustOneAPI's Douyin Creator Marketplace (Xingtu) audience distribution endpoint for creator evaluation, campaign planning, and marketplace research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a JustOneAPI token in command arguments and request URLs, which can expose it through process listings, shell history, URL logs, or request logs.

Mitigation: Use scoped or short-lived tokens where available, avoid environments that log process arguments or full URLs, and rotate the token if exposure is suspected.

Risk: The endpoint can return creator audience distribution data that may be sensitive in campaign planning or marketplace research contexts.

Mitigation: Limit access to users who need creator analytics data and avoid pasting raw responses into public chats, tickets, or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-data-sp-author-audience-distribution)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_audience_distribution&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_audience_distribution&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes the endpoint response first, then can return raw JSON; backend errors include the operation ID and backend payload.]

## Skill Version(s):

1.0.0 (source: server release evidence, published 2026-04-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
