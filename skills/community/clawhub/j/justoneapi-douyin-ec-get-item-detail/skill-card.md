## Description: <br>
Call GET /api/douyin-ec/get-item-detail/v1 for Douyin E-commerce Item Details through JustOneAPI with itemId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and analysts use this skill to call JustOneAPI's Douyin E-commerce item-detail endpoint with an itemId. It helps summarize returned product details such as price, title, and stock for product monitoring or competitive analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token and sends it to the JustOneAPI service. <br>
Mitigation: Use a revocable token, avoid logging full request URLs, and rotate the token if a URL containing it may have been exposed. <br>


## Reference(s): <br>
- [JustOneAPI API homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_ec_get_item_detail&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_ec_get_item_detail&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-ec-get-item-detail) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands] <br>
**Output Format:** [Markdown summary followed by raw JSON from the API helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and an itemId; backend errors should include the backend payload and operation ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
