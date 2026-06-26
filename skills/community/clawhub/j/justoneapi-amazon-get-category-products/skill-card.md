## Description: <br>
Call GET /api/amazon/get-category-products/v1 for Amazon Products By Category through JustOneAPI with categoryId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call JustOneAPI's Amazon category-products endpoint with a categoryId and summarize returned product data such as title, price, and rating. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is passed as a request URL query parameter and may be captured by logs. <br>
Mitigation: Use a limited, rotatable token where possible, avoid sharing token values in chat or logs, and rotate the token if exposure is suspected. <br>
Risk: The skill depends on a third-party JustOneAPI service for Amazon product lookup. <br>
Mitigation: Install and use it only when you trust JustOneAPI and are comfortable sending lookup parameters and the API token to that service. <br>


## Reference(s): <br>
- [JustOneAPI API Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_category_products&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_category_products&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, API calls, JSON, guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the getProductsByCategoryV1 operation and returns endpoint-specific Amazon product fields.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
