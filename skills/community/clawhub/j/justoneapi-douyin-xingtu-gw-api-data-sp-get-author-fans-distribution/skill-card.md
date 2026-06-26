## Description: <br>
Call GET /api/douyin-xingtu/gw/api/data_sp/get_author_fans_distribution/v1 for Douyin Creator Marketplace (Xingtu) Follower Distribution through JustOneAPI with oAuthorId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve Douyin Creator Marketplace follower distribution data for a creator by oAuthorId. The returned audience, location, and demographic breakdowns support creator evaluation, campaign planning, and marketplace research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent to api.justoneapi.com as a URL query parameter for this lookup. <br>
Mitigation: Provide the token through JUST_ONE_API_TOKEN, avoid sharing full request URLs or logs, and rotate or scope the token when your JustOneAPI account supports it. <br>
Risk: The skill depends on a third-party API and a valid JustOneAPI account token. <br>
Mitigation: Confirm the token source and endpoint need before use, and handle backend errors without exposing credentials or sensitive creator identifiers. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-data-sp-get-author-fans-distribution) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_fans_distribution&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_fans_distribution&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance, Shell commands] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and oAuthorId; optional authorType accepts FAN or DIE_HARD_FAN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
