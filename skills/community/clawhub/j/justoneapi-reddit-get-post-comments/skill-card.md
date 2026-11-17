## Description:

Call GET /api/reddit/get-post-comments/v1 for Reddit Post Comments through JustOneAPI with postId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI's Reddit comments endpoint for a specific postId, then summarize comment text, authors, timestamps, and pagination results for discussion analysis or moderation research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token can be exposed through request URLs or process logs.

Mitigation: Use a narrowly scoped, revocable JUST_ONE_API_TOKEN, avoid logging full commands or request URLs, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_reddit_get_post_comments&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_reddit_get_post_comments&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON from the API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a Reddit postId; optional cursor supports pagination.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
