## Description: <br>
Call GET /api/douyin-xingtu/gw/api/aggregator/get_author_commerce_spread_info/v1 for Douyin Creator Marketplace (Xingtu) Author Commerce Spread Info through JustOneAPI with oAuthorId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Douyin Creator Marketplace (Xingtu) author commerce spread metrics through JustOneAPI for creator evaluation, campaign planning, and media buying workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token for requests to the endpoint. <br>
Mitigation: Use a scoped or revocable token, avoid exposing token-bearing URLs or logs, and rotate the token if exposure is suspected. <br>
Risk: Backend error payloads may include request context that should not be broadly shared. <br>
Mitigation: Review command output before pasting it into chat, tickets, screenshots, or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-aggregator-get-author-commerce-spread-info) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_aggregator_get_author_commerce_spread_info&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_aggregator_get_author_commerce_spread_info&utm_content=project_link) <br>
- [Generated operations reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown summary with endpoint details and raw JSON response when the API call succeeds] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and the oAuthorId query parameter; no request body is documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
