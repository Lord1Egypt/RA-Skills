## Description:

Call GET /api/zhihu/get-column-article-detail/v1 for Zhihu Column Article Details through JustOneAPI with id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to retrieve Zhihu column article details by article id through JustOneAPI, supporting article archiving and content research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command arguments, request URLs, shell tracing, or process and proxy logs.

Mitigation: Use a narrowly scoped or low-risk token when available, avoid logging full commands or URLs, restrict access to process and proxy logs, and rotate the token if it may have been exposed.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_get_column_article_detail&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_get_column_article_detail&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a Zhihu article id.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
