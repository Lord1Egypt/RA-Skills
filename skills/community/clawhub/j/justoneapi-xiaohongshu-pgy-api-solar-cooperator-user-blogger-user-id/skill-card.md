## Description: <br>
Call GET /api/xiaohongshu-pgy/api/solar/cooperator/user/blogger/userId/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Profile through JustOneAPI with userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and marketing operations teams use this skill to look up Xiaohongshu Creator Marketplace creator profile data by userId for influencer vetting, benchmark analysis, and campaign planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JUST_ONE_API_TOKEN and sends creator-profile lookup requests to JustOneAPI. <br>
Mitigation: Treat the token as sensitive, avoid exposing it in chat, logs, screenshots, or process listings, and rotate it if exposure is suspected. <br>
Risk: Creator profile results may inform influencer vetting, benchmark analysis, and campaign planning decisions. <br>
Mitigation: Use the output only for authorized workflows and review the returned data before relying on it for campaign decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-api-solar-cooperator-user-blogger-user-id) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_cooperator_user_blogger_user_id&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_cooperator_user_blogger_user_id&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, JSON] <br>
**Output Format:** [Markdown guidance with a Node command example, endpoint-specific summary text, and raw JSON API output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node, JUST_ONE_API_TOKEN, and a userId query parameter for the documented v1 GET endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
