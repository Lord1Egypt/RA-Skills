## Description:

Call GET /api/weibo/get-weibo-detail/v1 for Weibo Post Details through JustOneAPI with id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch Weibo post detail data from JustOneAPI by post id, including media, author metadata, and engagement counts for analysis, archiving, and campaign monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a JustOneAPI token to api.justoneapi.com for credentialed Weibo lookup requests.

Mitigation: Use a limited, revocable token and install only when sharing that token with JustOneAPI is acceptable.

Risk: Tokens or request details may be exposed through command history, process metadata, screenshots, or logs.

Mitigation: Avoid pasting token values into chat or screenshots, limit log sharing, and rotate the token if exposure is possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-weibo-get-weibo-detail)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_weibo_detail&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_weibo_detail&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a Weibo post id.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
