## Description: <br>
Call GET /api/tiktok-shop/search-products/v1 for TikTok Shop Product Search through JustOneAPI with keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search TikTok Shop products by keyword through JustOneAPI for market research, trend analysis, competitor product discovery, and regional product popularity monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a JustOneAPI token, and server evidence warns that token handling can expose it more than users may expect. <br>
Mitigation: Use a protected environment variable or secret channel for JUST_ONE_API_TOKEN, avoid placing token values in chat, screenshots, logs, URLs, or process listings when possible, and rotate the token if exposure is suspected. <br>
Risk: The release was flagged suspicious by server security evidence because token misuse could have account access or billing impact. <br>
Mitigation: Review the skill before installation when the token has meaningful account access or billing impact, and prefer versions that read the token directly from protected secret storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-tiktok-shop-search-products) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_shop_search_products&utm_content=project_link) <br>
- [TikTok Shop Product Search operations](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and the JUST_ONE_API_TOKEN environment variable; accepts keyword plus optional region, offset, and pageToken query parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
