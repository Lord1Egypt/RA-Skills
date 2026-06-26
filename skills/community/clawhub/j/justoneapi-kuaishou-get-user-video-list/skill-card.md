## Description: <br>
Call GET /api/kuaishou/get-user-video-list/v2 for Kuaishou User Published Videos through JustOneAPI with userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to fetch Kuaishou published-video data by userId through JustOneAPI. It supports creator monitoring and content performance analysis with covers, publish times, and engagement metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive JustOneAPI token. <br>
Mitigation: Keep JUST_ONE_API_TOKEN in the environment and avoid pasting token values into chats, screenshots, logs, command histories, or URLs. <br>
Risk: The skill sends requests to api.justoneapi.com. <br>
Mitigation: Install and use it only if you trust JustOneAPI and are comfortable sending the token and request parameters to that service. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-kuaishou-get-user-video-list) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_user_video_list&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_user_video_list&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a Kuaishou userId; optional pcursor supports pagination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
