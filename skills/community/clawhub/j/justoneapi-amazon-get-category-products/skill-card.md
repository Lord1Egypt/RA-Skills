## Description:

Call GET /api/amazon/get-category-products/v1 for Amazon Products By Category through JustOneAPI with categoryId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to call JustOneAPI's Amazon category-products endpoint with a categoryId and optional country, page, and sort filters. It supports category-based product discovery by returning and summarizing product information such as title, price, and rating.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token and lookup parameters are sent to api.justoneapi.com.

Mitigation: Install only if this data sharing is acceptable for the intended use case.

Risk: The API token may be exposed through command lines, request URLs, shared shells, or CI logs.

Mitigation: Use a scoped, rotatable token, avoid shared shell and CI log exposure, and rotate the token if it may have been recorded.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-amazon-get-category-products)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_category_products&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_category_products&utm_content=project_link)
- [Generated Operations](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, json, guidance]

**Output Format:** [Markdown summary followed by raw JSON when endpoint results are available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should state the operation ID and endpoint path, echo the categoryId lookup scope, and prioritize title, price, and rating fields.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
