## Description:

Call GET /api/douyin-xingtu/gw/api/gauthor/get_author_content_hot_keywords/v1 for Douyin Creator Marketplace (Xingtu) KOL Content Keyword Analysis through JustOneAPI with oAuthorId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call a focused JustOneAPI endpoint for Douyin Creator Marketplace (Xingtu) creator content keyword analysis using an author ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a JustOneAPI token in ways that can expose it through process arguments and URL logs.

Mitigation: Use a short-lived or restricted token, avoid shared systems where process arguments may be monitored, and rotate the token if command logs, process listings, proxy logs, or API gateway logs may have captured it.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_gauthor_get_author_content_hot_keywords&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-gauthor-get-author-content-hot-keywords)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Endpoint-specific summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and oAuthorId.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
