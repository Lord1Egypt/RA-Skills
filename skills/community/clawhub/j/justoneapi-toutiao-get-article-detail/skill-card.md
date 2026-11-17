## Description:

Call GET /api/toutiao/get-article-detail/v1 for Toutiao Article Details through JustOneAPI with id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and media-monitoring workflows use this skill to fetch Toutiao article details by article ID through JustOneAPI and summarize metadata such as article ID, title, and author information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command-line arguments, shell history, process lists, or URL query logs.

Mitigation: Use a narrowly scoped and revocable token, avoid shell tracing and command logging, and rotate the token if it may have appeared in logs, process lists, URLs, or telemetry.

Risk: A JustOneAPI token with billing impact, broad access, or long validity increases the consequence of accidental exposure.

Mitigation: Review token scope, account permissions, and usage limits before installation, and revoke or rotate credentials when they are no longer needed.

## Reference(s):

- [Toutiao Article Details API on ClawHub](https://clawhub.ai/justoneapi/skills/justoneapi-toutiao-get-article-detail)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao_get_article_detail&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao_get_article_detail&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Short human-readable summary followed by raw JSON when endpoint data is returned; JSON error payloads for helper failures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a JustOneAPI token supplied through JUST_ONE_API_TOKEN or the helper's token argument.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
