## Description:

Call GET /api/bilibili/get-user-detail/v2 for Bilibili User Profile through JustOneAPI with uid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external API users use this skill to look up a Bilibili user profile by UID through JustOneAPI and summarize account metadata, audience metrics, and verification-related fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Bilibili UID and JUST_ONE_API_TOKEN are sent to JustOneAPI when the lookup runs.

Mitigation: Use a scoped, revocable token, avoid logging full commands or token values, and rotate the token if it may have appeared in logs.

Risk: Returned profile data could be misused for identity or trust decisions without enough context.

Mitigation: Use profile data only with appropriate consent and context, and do not treat it as standalone identity or trust proof.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_detail&utm_content=project_link)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_detail&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-bilibili-get-user-detail)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summary with optional raw JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a Bilibili uid.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
