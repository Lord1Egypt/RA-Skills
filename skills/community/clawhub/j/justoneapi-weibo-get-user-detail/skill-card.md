## Description:

Call GET /api/weibo/get-user-detail/v3 for Weibo User Profile through JustOneAPI with uid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent workflows use this skill to look up Weibo user profile data through JustOneAPI by UID, then summarize follower counts, verification status, bio details, and related account-analysis fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A JustOneAPI token is required and may be exposed through command-line, URL, or process logs.

Mitigation: Use a narrowly scoped, revocable token, avoid shared machines and verbose process logging, and rotate the token if logs may have captured it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-weibo-get-user-detail)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_user_detail&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_user_detail&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown summary with an optional shell command and raw JSON response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a Weibo uid; no request body is documented.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
