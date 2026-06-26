## Description: <br>
Call GET /api/tiktok-shop/get-product-detail/v1 for TikTok Shop Product Details through JustOneAPI with productId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve TikTok Shop product detail data by productId through JustOneAPI, including fields useful for catalogs, price and stock monitoring, and product analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens and queried product IDs are sent to JustOneAPI. <br>
Mitigation: Use the skill only when JustOneAPI is trusted for those product IDs and the API token. <br>
Risk: The JustOneAPI token could be exposed through chat, screenshots, logs, or command history. <br>
Mitigation: Use a scoped or rotatable token, pass it through JUST_ONE_API_TOKEN, avoid pasting token values into chat or logs, and avoid shared machines with command logging. <br>
Risk: The optional region parameter defaults to US, which may query the wrong market. <br>
Mitigation: Set region explicitly when the intended market is GB, SG, MY, PH, TH, VN, ID, or another supported non-US value. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-tiktok-shop-get-product-detail) <br>
- [JustOneAPI API Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_shop_get_product_detail&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_shop_get_product_detail&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses productId as the required lookup parameter and supports an optional region parameter that defaults to US.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
