## Description:

Call GET /api/weixin/get-article-feedback/v1 for WeChat Official Accounts Article Engagement Metrics through JustOneAPI with articleUrl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve engagement metrics for a WeChat Official Accounts article URL through JustOneAPI, including like, share, and comment data for performance tracking and benchmarking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required API token may be exposed through process metadata or request URL logs because the helper accepts it on the command line and sends it as a query parameter.

Mitigation: Use a narrowly scoped, revocable JUST_ONE_API_TOKEN, avoid shared or heavily monitored environments, and rotate the token after use when exposure is possible.

Risk: Security evidence marks this release suspicious due to token-handling exposure despite matching the stated API behavior.

Mitigation: Review the skill before installing and prefer a release that reads credentials from protected environment or standard input and sends authentication in a header if the API supports it.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_article_feedback&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_article_feedback&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON]

**Output Format:** [Markdown summary with endpoint details and raw JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and an articleUrl query parameter.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
