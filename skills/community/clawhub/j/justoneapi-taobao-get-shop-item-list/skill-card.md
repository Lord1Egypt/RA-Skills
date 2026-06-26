## Description: <br>
Call 3 get-shop-item-list versions for Taobao and Tmall Shop Product List through JustOneAPI with shopId and userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and marketplace operators use this skill to call JustOneAPI endpoints that retrieve Taobao and Tmall shop product lists for seller research and catalog tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent in the request URL query string. <br>
Mitigation: Use a scoped token when available, avoid sharing command lines or logs that may contain the token, and rotate the token if exposure is suspected. <br>
Risk: The skill requires sensitive credentials and shop or user identifiers for a third-party API provider. <br>
Mitigation: Install only when the publisher and JustOneAPI are trusted for the token and identifiers provided. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-taobao-get-shop-item-list) <br>
- [JustOneAPI API Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_get_shop_item_list&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_get_shop_item_list&utm_content=project_link) <br>
- [Generated Operations Reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and Taobao/Tmall shop identifiers; responses should include the operation ID and endpoint path used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
