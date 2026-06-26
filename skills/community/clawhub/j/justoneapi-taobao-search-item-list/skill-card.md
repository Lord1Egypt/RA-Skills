## Description: <br>
Call GET /api/taobao/search-item-list/v1 for Taobao and Tmall Product Search through JustOneAPI with keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to search Taobao and Tmall products through JustOneAPI by keyword, with optional sorting, Tmall-only filtering, price bounds, and pagination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token and sends product search requests to api.justoneapi.com. <br>
Mitigation: Install only if you trust JustOneAPI, use a dedicated rotatable token, and avoid sending sensitive search terms. <br>
Risk: Tokens, full command lines, request URLs, or backend payloads may be exposed through chat, screenshots, shell history, shared terminals, or debug logs. <br>
Mitigation: Pass the token from JUST_ONE_API_TOKEN, avoid pasting token values into shared contexts, and review logs before sharing them. <br>


## Reference(s): <br>
- [Generated Operation Reference](generated/operations.md) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_search_item_list&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_search_item_list&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-taobao-search-item-list) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, JSON] <br>
**Output Format:** [Markdown summary followed by raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the searchItemListV1 operation and returns endpoint-specific results or backend error payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
