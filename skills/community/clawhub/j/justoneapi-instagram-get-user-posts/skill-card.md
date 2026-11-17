## Description:

Call GET /api/instagram/get-user-posts/v1 for Instagram User Published Posts through JustOneAPI with username.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve published Instagram posts for a specific username through JustOneAPI, then summarize post fields such as code, caption, and media type for monitoring, auditing, or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through process arguments or URL logs.

Mitigation: Use a restricted or short-lived token where possible, avoid shared systems where command arguments may be visible, and review infrastructure logging before use.

Risk: Retrieved Instagram data may be subject to platform, provider, or legal restrictions.

Mitigation: Use returned post data only where lawful and consistent with Instagram and JustOneAPI terms.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_user_posts&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_user_posts&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-instagram-get-user-posts)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with optional raw JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and an Instagram username; paginationToken is optional.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
