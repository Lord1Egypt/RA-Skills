## Description: <br>
Call GET /api/douyin-xingtu/get-kol-link-struct/v1 for Douyin Creator Marketplace (Xingtu) Creator Link Structure through JustOneAPI with kolId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a JustOneAPI Douyin Creator Marketplace (Xingtu) endpoint for a creator's link structure metrics by KOL ID. It supports creator performance analysis by returning an endpoint-specific summary followed by raw JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a query parameter and could appear in URLs, logs, shell history, screenshots, or monitoring tools. <br>
Mitigation: Keep JUST_ONE_API_TOKEN private, avoid sharing full request URLs or command output, and rotate the token if it may have been exposed. <br>
Risk: The skill performs a live third-party API lookup for Douyin/Xingtu creator data. <br>
Mitigation: Install and run it only when the user trusts JustOneAPI with the lookup parameters and the API token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-get-kol-link-struct) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_link_struct&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_link_struct&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON from the API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; required endpoint input is kolId, with optional acceptCache.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
