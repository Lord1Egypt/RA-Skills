## Description:

Call GET /api/tiktok/get-user-detail/v1 through JustOneAPI to retrieve TikTok profile data such as nickname, unique ID, avatar, and verification status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up TikTok user profile details through JustOneAPI for influencer profiling, audience analysis, account tracking, and identifying verified or official accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token and TikTok lookup parameters are sent to api.justoneapi.com, and the token is passed through the command line and URL query string.

Mitigation: Use a narrowly scoped token when available, avoid exposing token values in chats, screenshots, logs, shell history, or process telemetry, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_user_detail&utm_content=project_link)
- [TikTok User Profile API on ClawHub](https://clawhub.ai/justoneapi/skills/justoneapi-tiktok-get-user-detail)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and accepts optional uniqueId or secUid query parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
