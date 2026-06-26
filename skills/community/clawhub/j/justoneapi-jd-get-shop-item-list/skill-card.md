## Description: <br>
Call GET /api/jd/get-shop-item-list/v1 for JD.com Shop Product List through JustOneAPI with shopId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to fetch JD.com shop product-list data through JustOneAPI for catalog tracking and seller research. It requires a JustOneAPI token and a JD.com shopId, with optional pagination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sensitive and is sent as a query parameter in the request URL. <br>
Mitigation: Use a revocable, least-privilege token; avoid sharing command output or URLs that may contain the token; rotate the token if it may have appeared in logs or terminal history. <br>
Risk: The skill depends on external JustOneAPI and JD.com endpoint behavior, so backend failures or schema changes can affect results. <br>
Mitigation: Check backend error payloads, operation IDs, and response JSON before using results in downstream workflows. <br>


## Reference(s): <br>
- [JustOneAPI API Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd_get_shop_item_list&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd_get_shop_item_list&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-jd-get-shop-item-list) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes endpoint use and should return raw JSON after a short endpoint-specific summary; backend errors include the operation ID and backend payload.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
