## Description: <br>
Call GET /api/douyin/search-user/v2 for Douyin (TikTok China) User Search through JustOneAPI with keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search Douyin user accounts by keyword through JustOneAPI and summarize profile metadata and follower signals for creator discovery or account research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a URL query parameter and may appear in logs if full request URLs or command invocations are captured. <br>
Mitigation: Use a scoped, rotatable JUST_ONE_API_TOKEN, avoid logging full request URLs or token-bearing commands, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-search-user) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_search_user&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_search_user&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and summarized API JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, JUST_ONE_API_TOKEN, and a keyword query; optional page and userType filters are supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
