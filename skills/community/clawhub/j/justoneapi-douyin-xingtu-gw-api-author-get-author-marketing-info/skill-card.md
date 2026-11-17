## Description:

Call GET /api/douyin-xingtu/gw/api/author/get_author_marketing_info/v1 for Douyin Creator Marketplace (Xingtu) Marketing Metrics through JustOneAPI with oAuthorId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and marketing analysts use this skill to call a focused JustOneAPI endpoint for Douyin Creator Marketplace creator marketing metrics. It supports creator evaluation, campaign planning, marketplace research, and review of rate-card or commercial-service metrics for a supplied author ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a JustOneAPI token to api.justoneapi.com and handles the token in exposure-prone ways.

Mitigation: Use a narrowly scoped, revocable token and install only when sending that token to api.justoneapi.com is acceptable.

Risk: Token values may be exposed on shared machines where process arguments can be inspected.

Mitigation: Avoid running the helper on shared machines and do not paste token values into chat messages, screenshots, or logs.

Risk: Returned creator marketing metrics and rate-card data may be business-sensitive.

Mitigation: Limit access to returned data and handle API responses according to the user's business-data policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-author-get-author-marketing-info)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_author_get_author_marketing_info&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_author_get_author_marketing_info&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN; the endpoint requires oAuthorId and accepts an optional platform query value.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
