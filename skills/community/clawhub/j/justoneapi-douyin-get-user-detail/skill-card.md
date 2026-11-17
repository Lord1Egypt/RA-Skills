## Description:

Call GET /api/douyin/get-user-detail/v3 for Douyin (TikTok China) User Profile through JustOneAPI with secUid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call JustOneAPI's Douyin user profile endpoint for creator research and account analysis using a Douyin secUid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is passed through command-line arguments and as a URL query parameter, which can expose credentials in process listings, shell history, command logs, or URL logs.

Mitigation: Use a short-lived or low-scope token, avoid shared shells and logged automation, do not paste token values into chat or logs, and rotate the token if it may have been exposed.

Risk: Using the endpoint sends Douyin secUid lookup values and the JustOneAPI token to JustOneAPI.

Mitigation: Use the skill only when that data sharing is acceptable for the user's workflow and policy requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-get-user-detail)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_user_detail&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_user_detail&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Endpoint-specific summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, JUST_ONE_API_TOKEN, and secUid.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
