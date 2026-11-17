## Description:

Call GET /api/douyin/get-user-video-list/v3 for Douyin (TikTok China) User Published Videos through JustOneAPI with secUid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call JustOneAPI's Douyin user published videos endpoint with a Douyin secUid and optional pagination cursor, then summarize captions, covers, publish times, and related response data for account monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token and Douyin lookup data may be exposed through command lines, logs, screenshots, or process telemetry.

Mitigation: Use a least-privilege, revocable token where available, avoid sharing run logs or screenshots containing commands, and rotate the token if exposure is suspected.

Risk: Use of this skill sends the requested Douyin account lookup data to JustOneAPI.

Mitigation: Install and use the skill only when the publisher and API service are trusted for the token and lookup data being submitted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-get-user-video-list)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_user_video_list&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_user_video_list&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JUST_ONE_API_TOKEN, requires Node.js, and returns raw JSON after a short endpoint-specific summary.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
