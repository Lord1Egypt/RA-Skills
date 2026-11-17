## Description:

Call GET /api/kuaishou/get-user-detail/v1 for Kuaishou User Profile through JustOneAPI with userId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI's Kuaishou user profile endpoint for creator research, creator profile building, and monitoring audience growth or account status by userId.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a JustOneAPI access token and sends it as a query parameter to the Kuaishou profile endpoint.

Mitigation: Use a scoped token if available, avoid logging command lines or full request URLs, and rotate the token if it may have been exposed.

Risk: Returned creator profile data may include account metadata, audience metrics, and verification-related fields that could be sensitive.

Mitigation: Limit lookups to intended use cases and handle returned profile data according to applicable privacy and data-handling requirements.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_user_detail&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_user_detail&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-kuaishou-get-user-detail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, JSON]

**Output Format:** [Markdown summary followed by raw JSON when results are available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; accepts userId as the required non-token query parameter.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
