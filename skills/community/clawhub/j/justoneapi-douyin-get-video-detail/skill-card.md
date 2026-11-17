## Description:

Call GET /api/douyin/get-video-detail/v2 for Douyin (TikTok China) Video Details through JustOneAPI with videoId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve Douyin video details by videoId through JustOneAPI for video research, archiving, and performance analysis. The response supports summaries of author details, publish time, engagement counts, and the raw backend JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A JustOneAPI token can be exposed if process arguments, full request URLs, chat messages, screenshots, or logs are captured.

Mitigation: Pass the token from JUST_ONE_API_TOKEN, run in an environment that does not log process arguments or full request URLs, avoid pasting tokens into chat or logs, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-get-video-detail)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_video_detail&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_video_detail&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a videoId query parameter; backend errors should include the backend payload and operation ID.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
