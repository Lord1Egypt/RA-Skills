## Description:

Call GET /api/youtube/get-video-detail/v1 for YouTube Video Details through JustOneAPI with videoId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve YouTube video metadata from JustOneAPI by videoId for content analysis, engagement tracking, and availability checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through URLs and process arguments.

Mitigation: Use a narrowly scoped or disposable token if available, avoid sharing logs or process telemetry from runs, and rotate the token if exposure is possible.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youtube_get_video_detail&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youtube_get_video_detail&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the operation ID, endpoint path, videoId lookup scope, and backend error payloads when calls fail.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
