## Description: <br>
Call GET /api/amazon/get-product-detail/v1 for Amazon Product Details through JustOneAPI with asin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to fetch Amazon product detail data by ASIN through JustOneAPI for catalog enrichment, price monitoring, availability tracking, and e-commerce analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent to api.justoneapi.com as a URL query parameter. <br>
Mitigation: Use a limited or revocable token if available, avoid sharing command output or logs that may include request URLs, and rotate the token if it may have been logged. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/justoneapi/justoneapi-amazon-get-product-detail) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_product_detail&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_product_detail&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with a Node.js command and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses getAmazonProductDetailV1 with required asin, optional country, and JUST_ONE_API_TOKEN authentication.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
