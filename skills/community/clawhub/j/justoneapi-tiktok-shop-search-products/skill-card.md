## Description:

Call GET /api/tiktok-shop/search-products/v1 for TikTok Shop Product Search through JustOneAPI with keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search TikTok Shop products through JustOneAPI by keyword for market research, trend analysis, competitor product discovery, and product popularity monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a JustOneAPI token, and tokens can be exposed through copied commands, full request URLs, screenshots, or logs.

Mitigation: Pass the token through JUST_ONE_API_TOKEN, avoid logging full command lines or request URLs, keep access scoped to the minimum available, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI API homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_shop_search_products&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_shop_search_products&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-tiktok-shop-search-products)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a keyword; optional query parameters include region, offset, and pageToken.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
