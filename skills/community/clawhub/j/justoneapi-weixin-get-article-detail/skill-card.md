## Description:

Call GET /api/weixin/get-article-detail/v1 for WeChat Official Accounts Article Details through JustOneAPI with articleUrl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and content analysts use this skill to retrieve WeChat Official Accounts article details, including body content, through JustOneAPI for article archiving, research, and content analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through process arguments, shell history, process telemetry, or URL query logs.

Mitigation: Use a narrowly scoped, revocable token; avoid pasting token values into chat, screenshots, or logs; and rotate the token if exposure is suspected.

Risk: The API call may have billing or permission impact when the token has broad account access.

Mitigation: Review account permissions and billing limits before installation, and prefer a token dedicated to this endpoint or workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-weixin-get-article-detail)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_article_detail&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_article_detail&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Markdown summary with endpoint details and raw JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and articleUrl; backend errors include the operation ID and backend payload when available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
