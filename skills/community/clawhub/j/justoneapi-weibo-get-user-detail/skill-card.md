## Description: <br>
Call GET /api/weibo/get-user-detail/v3 for Weibo User Profile through JustOneAPI with uid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to look up Weibo profile details by uid through JustOneAPI, including follower counts, verification status, and bio details for creator research and account analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token can be exposed through command arguments and request URLs. <br>
Mitigation: Use a protected environment or secret store, avoid shared systems that log process arguments or URLs, and never paste token values into chat, screenshots, or logs. <br>
Risk: The requested Weibo uid and JustOneAPI token are sent to JustOneAPI. <br>
Mitigation: Install and run this skill only when that data transfer is acceptable for the user, organization, and use case. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-weibo-get-user-detail) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_user_detail&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_user_detail&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, configuration] <br>
**Output Format:** [Markdown guidance with an endpoint-specific summary and raw JSON response data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, JUST_ONE_API_TOKEN, and a Weibo uid query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
