## Description: <br>
Call GET /api/tiktok/get-user-post/v1 for TikTok User Published Posts through JustOneAPI with secUid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to fetch TikTok published-post data for a specific secUid through JustOneAPI. The results support creator activity analysis, posting frequency review, influencer performance evaluation, and content trend monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token and TikTok secUid are sent to JustOneAPI when this endpoint is called. <br>
Mitigation: Install and run the skill only when this data sharing is acceptable, and use a limited-scope or disposable token if available. <br>
Risk: Credential values may be exposed if full request URLs, commands, screenshots, or diagnostics are shared. <br>
Mitigation: Pass the token through JUST_ONE_API_TOKEN or the token argument without pasting token values into shared materials, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-tiktok-get-user-post) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_user_post&utm_content=project_link) <br>
- [TikTok User Published Posts operations](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with JSON response data and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and secUid; optional cursor and sort query parameters are passed through to JustOneAPI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
