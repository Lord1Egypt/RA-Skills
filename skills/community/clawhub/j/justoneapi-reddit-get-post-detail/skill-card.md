## Description:

Call GET /api/reddit/get-post-detail/v1 for Reddit Post Details through JustOneAPI with postId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and moderation teams use this skill to retrieve Reddit post details by postId through JustOneAPI, including author, subreddit, and engagement data for content analysis, moderation research, and monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command-line process data or URL query logs.

Mitigation: Use a narrowly scoped token, avoid logging full URLs or process arguments, and rotate the token if exposure is possible.

Risk: The skill requires account access or paid quota through JUST_ONE_API_TOKEN.

Mitigation: Review the skill before installing and use a protected environment source for credentials where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-reddit-get-post-detail)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_reddit_get_post_detail&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_reddit_get_post_detail&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN; calls one GET endpoint with postId as a query parameter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
