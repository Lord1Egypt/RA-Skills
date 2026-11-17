## Description:

Call GET /api/zhihu/get-column-article-list/v1 for Zhihu Column Article List through JustOneAPI with columnId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Zhihu column article lists through JustOneAPI for column monitoring and content collection when they have a JustOneAPI token and a columnId.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token is sent as a URL query parameter, which may expose it in provider, proxy, gateway, diagnostic, command-line, or log records.

Mitigation: Use a narrowly scoped, revocable JustOneAPI token; avoid sharing command lines or logs that contain the token; rotate the token if URL logging exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-zhihu-get-column-article-list)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_get_column_article_list&utm_content=project_link)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_get_column_article_list&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON]

**Output Format:** [Markdown summary with optional shell command and JSON response payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and the columnId query parameter; offset is optional.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
