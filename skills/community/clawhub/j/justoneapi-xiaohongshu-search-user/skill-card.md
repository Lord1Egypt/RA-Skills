## Description: <br>
Call GET /api/xiaohongshu/search-user/v2 for Xiaohongshu (RedNote) User Search through JustOneAPI with keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to search Xiaohongshu (RedNote) users by keyword through JustOneAPI for creator discovery and account research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search keywords and a JustOneAPI token to JustOneAPI. <br>
Mitigation: Use the skill only when that data sharing is acceptable, avoid sensitive search terms, and use a dedicated revocable token. <br>
Risk: The token may be exposed through command lines, shared terminals, shell history, proxies, or logs. <br>
Mitigation: Pass the token from the environment, avoid pasting token values into chat or logs, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-search-user) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_user&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_user&utm_content=project_link) <br>
- [Generated operation reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN; the endpoint accepts keyword and optional page query parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
