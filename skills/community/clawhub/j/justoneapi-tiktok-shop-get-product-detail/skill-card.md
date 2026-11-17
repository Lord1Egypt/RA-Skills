## Description:

Call GET /api/tiktok-shop/get-product-detail/v1 for TikTok Shop Product Details through JustOneAPI with productId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve TikTok Shop product details by product ID through JustOneAPI, including fields useful for product catalogs, price and stock monitoring, and product analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a JustOneAPI token, and the security evidence warns that passing tokens through command arguments or request URLs can expose them in logs or process listings.

Mitigation: Use a narrowly scoped, revocable token when available, avoid logging commands or request URLs, and rotate the token after testing or suspected exposure.

Risk: The security evidence says the skill lacks explicit network and tool scoping.

Mitigation: Run it only in environments where outbound access to JustOneAPI is expected and review the command before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-tiktok-shop-get-product-detail)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_shop_get_product_detail&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_shop_get_product_detail&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Markdown summary followed by raw JSON from the API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN. The endpoint requires productId and accepts an optional region value.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
