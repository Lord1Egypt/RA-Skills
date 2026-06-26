## Description: <br>
Call GET /api/bilibili/get-user-video-list/v2 for Bilibili User Published Videos through JustOneAPI with uid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to call JustOneAPI's Bilibili user published videos endpoint by UID and summarize titles, covers, publish times, and pagination results for creator monitoring and content performance analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sensitive and is passed to the helper for the endpoint request. <br>
Mitigation: Keep the token in the JUST_ONE_API_TOKEN environment variable, avoid exposing command lines or logs that include it, and rotate the token if it may have been captured. <br>
Risk: The skill depends on a third-party API response for Bilibili video data. <br>
Mitigation: Review returned data before relying on it for decisions and include the backend payload when troubleshooting API errors. <br>


## Reference(s): <br>
- [JustOneAPI API Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_video_list&utm_content=project_link) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_video_list&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls] <br>
**Output Format:** [Markdown summary with optional raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a Bilibili uid; backend errors may include the backend payload and operation ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
