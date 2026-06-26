## Description: <br>
Call GET /api/douyin/get-video-detail/v2 for Douyin (TikTok China) Video Details through JustOneAPI with videoId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to retrieve Douyin video details by videoId, including author details, publish time, and engagement counts for research, archiving, and performance analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent to api.justoneapi.com and travels in the URL query string, which can expose it through full request URL logs. <br>
Mitigation: Use this skill only in environments where sending the token to api.justoneapi.com is acceptable, avoid logging full request URLs, and prefer a limited or disposable token when supported. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_video_detail&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_video_detail&utm_content=project_link) <br>
- [ClawHub skill listing](https://clawhub.ai/justoneapi/justoneapi-douyin-get-video-detail) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with optional raw JSON from the JustOneAPI response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; calls one GET endpoint with videoId.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
