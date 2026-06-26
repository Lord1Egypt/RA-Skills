## Description: <br>
Call GET /api/youtube/get-video-detail/v1 for YouTube Video Details through JustOneAPI with videoId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch YouTube video metadata through JustOneAPI by videoId for content analysis, engagement checks, and availability or status verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required JustOneAPI token may be exposed through process telemetry, request URLs, logs, or shared-system inspection. <br>
Mitigation: Use a limited and revocable token, avoid shared systems, do not paste token values into chat or logs, and prefer secure environment handling and Authorization-header transport if the provider supports it. <br>


## Reference(s): <br>
- [Generated operation reference](artifact/generated/operations.md) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youtube_get_video_detail&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Markdown summary with optional raw JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and a YouTube videoId.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
