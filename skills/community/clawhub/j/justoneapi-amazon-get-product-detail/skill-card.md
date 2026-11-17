## Description:

Call GET /api/amazon/get-product-detail/v1 for Amazon Product Details through JustOneAPI with asin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and e-commerce teams use this skill to look up Amazon product details by ASIN through JustOneAPI. It supports catalog enrichment, price and availability monitoring, and e-commerce analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command arguments or full request URLs.

Mitigation: Use a least-privilege token, avoid logging commands or full request URLs, and rotate the token if it may have appeared in logs.

Risk: A token with billing or broad account privileges increases impact if exposed.

Mitigation: Review the skill before installing and prefer credentials scoped only to the required Amazon product lookup operation.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_product_detail&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_product_detail&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown summary followed by raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the operation ID, endpoint path, echoed ASIN lookup scope, and backend error payloads when calls fail.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
