## Description:

Call GET /api/toutiao/get-user-detail/v1 for Toutiao User Profile through JustOneAPI with userId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Toutiao user profile details through JustOneAPI for influencer profiling, audience analysis, and creator performance monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token is handled as a command argument and query parameter.

Mitigation: Use a limited, rotatable token and avoid exposing token values in chat, screenshots, shell history, or logs.

Risk: The skill retrieves Toutiao profile data that may be subject to privacy or legal restrictions.

Mitigation: Use returned profile data only with appropriate authorization and a valid privacy and legal basis.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao_get_user_detail&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-toutiao-get-user-detail)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON when results are returned.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a Toutiao userId; returned profile data may include user ID, nickname, and avatar.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
