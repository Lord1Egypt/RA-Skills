## Description:

Call GET /api/instagram/get-user-detail/v1 for Instagram User Profile through JustOneAPI with username.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up public Instagram profile metadata, including follower, following, and post counts, by username through JustOneAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command-line arguments, full URLs, logs, shell history, process telemetry, proxy logs, or error reports.

Mitigation: Use a low-scope token where possible, avoid environments that log command lines or full URLs, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_user_detail&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_user_detail&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-instagram-get-user-detail)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with optional raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and an Instagram username; responses should identify the operation ID and endpoint path used.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
