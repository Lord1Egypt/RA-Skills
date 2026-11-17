## Description:

Call GET /api/weibo/get-user-post/v1 for Weibo User Published Posts through JustOneAPI with uid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call a JustOneAPI Weibo endpoint for published posts from a specific Weibo user ID. It supports account monitoring workflows that need post text, media, and publish time data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed unnecessarily because the skill handles it in query-token authentication flows.

Mitigation: Use a narrowly scoped token, avoid logging full request URLs, and monitor only accounts the user is permitted to monitor.

Risk: Tokens with broad quota, billing, or data access increase installation and runtime impact.

Mitigation: Review token scope before installing and prefer a version that reads the token directly from the environment and uses header-based authentication if the API supports it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-weibo-get-user-post)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_user_post&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_user_post&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes the endpoint response before returning raw JSON; backend errors include the backend payload and operation ID.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
