## Description:

Call GET /api/douyin-xingtu/gw/api/data/get_author_hot_comment_tokens/v1 for Douyin Creator Marketplace (Xingtu) KOL Comment Keyword Analysis through JustOneAPI with oAuthorId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call a focused JustOneAPI endpoint for Douyin Creator Marketplace (Xingtu) KOL comment keyword analysis by author ID. It supports audience language analysis and comment-topic research by returning endpoint results for the requested creator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is sent as a URL query parameter and may be captured by infrastructure, proxy, or service logs.

Mitigation: Use a narrowly scoped, revocable token and avoid logging full request URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-data-get-author-hot-comment-tokens)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_get_author_hot_comment_tokens&utm_content=project_link)
- [Generated operation reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with JSON response payloads and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and oAuthorId; raw JSON is returned after a short endpoint-specific summary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
