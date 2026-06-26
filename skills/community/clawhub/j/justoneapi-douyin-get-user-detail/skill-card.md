## Description: <br>
Call GET /api/douyin/get-user-detail/v3 for Douyin (TikTok China) User Profile through JustOneAPI with secUid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query JustOneAPI for Douyin user profile details by secUid, including follower counts, verification status, and bio details for creator research and account analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is required and is sent as a URL query parameter for this endpoint. <br>
Mitigation: Use a scoped or easily rotated token, avoid sharing request URLs or command output that may expose credentials, and rotate the token if it may have appeared in logs. <br>
Risk: The skill queries Douyin profile data for user-provided secUid values. <br>
Mitigation: Keep user-provided secUid values unchanged for correctness, but avoid sharing queried identifiers or returned profile data outside the intended workflow. <br>


## Reference(s): <br>
- [Generated operation reference](generated/operations.md) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_user_detail&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_user_detail&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-get-user-detail) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses operation getUserDetailV3 with required secUid and JUST_ONE_API_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
