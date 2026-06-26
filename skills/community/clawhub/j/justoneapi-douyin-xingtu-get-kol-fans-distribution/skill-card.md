## Description: <br>
Call GET /api/douyin-xingtu/get-kol-fans-distribution/v1 for Douyin Creator Marketplace (Xingtu) Follower Distribution through JustOneAPI with kolId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to request Douyin/Xingtu follower distribution data for a specified creator, including audience demographics, interests, and distribution metrics for creator evaluation, campaign planning, and marketplace research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthorized or inappropriate requests for Douyin/Xingtu audience analytics could expose creator-related marketplace data outside the user's allowed use. <br>
Mitigation: Use the skill only when you trust JustOneAPI and are authorized to request analytics for the submitted creator IDs. <br>
Risk: JUST_ONE_API_TOKEN may be exposed through chat, logs, screenshots, or full request URLs. <br>
Mitigation: Treat JUST_ONE_API_TOKEN as a secret, avoid logging full request URLs, and rotate the token if it is exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-get-kol-fans-distribution) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_fans_distribution&utm_content=project_link) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_fans_distribution&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON response data when the endpoint succeeds] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a kolId query parameter; optional fansType and acceptCache parameters refine the request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, published 2026-04-25T07:49:31Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
