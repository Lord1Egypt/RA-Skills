## Description:

Call GET /api/twitter/get-user-detail/v1 for Twitter User Profile through JustOneAPI with restId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to look up Twitter/X user profile metadata by restId through the JustOneAPI Twitter User Profile endpoint. It supports summaries of account metadata, audience counts, verification fields, and raw JSON responses from the API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token can be exposed through command lines or full request URLs.

Mitigation: Use a narrowly scoped, short-lived JustOneAPI token where possible, avoid shared or heavily logged environments, and rotate the token if logs may capture command lines or URLs.

Risk: The skill can retrieve Twitter/X profile data for a supplied restId.

Mitigation: Use it only for user-requested profile lookups and preserve the provided restId without expanding the lookup scope.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_twitter_get_user_detail&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_twitter_get_user_detail&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-twitter-get-user-detail)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Markdown summary followed by raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; uses restId as the required lookup parameter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
