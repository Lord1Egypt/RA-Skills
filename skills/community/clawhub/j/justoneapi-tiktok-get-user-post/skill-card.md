## Description:

Call GET /api/tiktok/get-user-post/v1 for TikTok User Published Posts through JustOneAPI with secUid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI's TikTok published-posts endpoint for a specific secUid and summarize video IDs, descriptions, publish times, and pagination results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can appear in command-line process metadata or service-side URL logs because it is passed as a CLI argument and query parameter.

Mitigation: Use a scoped token when available, avoid sharing command logs, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-tiktok-get-user-post)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_user_post&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_user_post&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses should provide a short endpoint-specific summary before raw JSON.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
