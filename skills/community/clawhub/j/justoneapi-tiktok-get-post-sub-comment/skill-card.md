## Description:

Call GET /api/tiktok/get-post-sub-comment/v1 for TikTok Comment Replies through JustOneAPI with awemeId and commentId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve TikTok comment replies for a specific post and parent comment through JustOneAPI. It supports threaded-discussion review by returning reply IDs, user information, text content, and related endpoint results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a JustOneAPI token for TikTok comment-reply lookups, creating a disclosed credential-handling risk.

Mitigation: Use a narrowly scoped or short-lived token, avoid shell tracing and shared machines, and rotate the token if process arguments or request URLs may have been logged.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-tiktok-get-post-sub-comment)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_post_sub_comment&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_post_sub_comment&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON]

**Output Format:** [Markdown summary with optional shell command guidance and raw JSON endpoint results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses operation getPostSubCommentV1 with required awemeId and commentId values and optional cursor pagination.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
