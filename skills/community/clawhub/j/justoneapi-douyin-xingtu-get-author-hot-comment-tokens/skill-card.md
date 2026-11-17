## Description:

Call GET /api/douyin-xingtu/get-author-hot-comment-tokens/v1 for Douyin Creator Marketplace (Xingtu) KOL Comment Keyword Analysis through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI's Douyin Creator Marketplace (Xingtu) endpoint for KOL comment keyword analysis by KOL ID, then summarize audience-language and comment-topic signals before returning raw JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the API token is handled through command-line arguments and URL query parameters, which may expose credentials through process lists or logs.

Mitigation: Use a narrowly scoped, revocable JustOneAPI token, avoid shared systems where process arguments may be visible, and ensure surrounding infrastructure redacts query parameters.

Risk: The security evidence marks the release verdict as suspicious and recommends review before installation.

Mitigation: Review and scan the skill before deployment, and confirm the helper behavior is acceptable for the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-author-hot-comment-tokens)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_author_hot_comment_tokens&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_author_hot_comment_tokens&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON from the API helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a kolId query parameter; optional acceptCache controls cache use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
