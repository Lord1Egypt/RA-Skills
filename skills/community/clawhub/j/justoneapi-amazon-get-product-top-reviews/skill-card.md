## Description: <br>
Call GET /api/amazon/get-product-top-reviews/v1 for Amazon Product Top Reviews through JustOneAPI with asin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to call JustOneAPI's Amazon product top reviews endpoint for an ASIN, optionally scoped by Amazon country marketplace, and summarize the JSON response for review research, sentiment analysis, and competitor feedback tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a URL query parameter, which can be exposed through command lines, logs, browser history, or request telemetry. <br>
Mitigation: Use a scoped or low-privilege token when available, avoid logging full URLs or command lines, and rotate the token if exposure is suspected. <br>
Risk: The skill depends on a third-party API service and returns data from that service without independent verification. <br>
Mitigation: Review API responses before using them in decisions, and include backend error payloads with the exact operation ID when calls fail. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_product_top_reviews&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-amazon-get-product-top-reviews) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary followed by JSON from the API helper when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and an ASIN; country defaults to US when omitted.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
