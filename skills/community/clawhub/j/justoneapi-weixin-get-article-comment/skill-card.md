## Description:

Call GET /api/weixin/get-article-comment/v1 for WeChat Official Accounts Article Comments through JustOneAPI with articleUrl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve WeChat Official Accounts article comments through JustOneAPI for feedback analysis, including commenter details, comment text, and timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is sent as a URL query parameter and may be captured in request logs, browser history, monitoring systems, or shared error output.

Mitigation: Use a short-lived, tightly scoped token, avoid sharing full request URLs or logs, and rotate the token if exposure is suspected.

Risk: The endpoint returns commenter details, comment text, and timestamps that may create privacy or compliance obligations.

Mitigation: Review data collection obligations before use, limit access to retrieved data, and retain only the fields needed for the feedback analysis task.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-weixin-get-article-comment)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_article_comment&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_article_comment&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with optional raw JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and an articleUrl query parameter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
