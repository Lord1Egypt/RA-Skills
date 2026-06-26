## Description: <br>
Call GET /api/douyin/get-video-sub-comment/v1 for Douyin (TikTok China) Comment Replies through JustOneAPI with commentId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to call a JustOneAPI Douyin endpoint for comment-reply data, including text, authors, and timestamps, using a required commentId and optional page parameter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token and sends it as a URL query parameter. <br>
Mitigation: Use a limited-scope or disposable token where possible, avoid exposing command lines or logs, and rotate the token if it may have been shared. <br>
Risk: The skill calls an external JustOneAPI endpoint and returns backend payloads. <br>
Mitigation: Install and run it only when you trust JustOneAPI and are comfortable sending the requested commentId and token to that service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-get-video-sub-comment) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_video_sub_comment&utm_content=project_link) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_video_sub_comment&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JUST_ONE_API_TOKEN credential and a commentId query parameter; page is optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
