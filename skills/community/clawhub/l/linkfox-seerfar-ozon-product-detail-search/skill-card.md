## Description:

Seerfar-Ozon商品详情 retrieves detailed Seerfar analytics for one Ozon SKU, including product identity, price, ratings, sales and revenue metrics, stock, category rank history, daily sales trend, brand, seller, fulfillment, weight, and listing age.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace researchers, ecommerce operators, and agent workflows use this skill to look up a single Ozon SKU and summarize product-level Seerfar analytics for listing diagnostics, competitor analysis, sales trend review, and category-rank tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on LinkFox-controlled endpoints and LINKFOX_* environment variables.

Mitigation: Install and run it only in an environment where the LinkFox endpoints are trusted and LINKFOX_* variables are controlled.

Risk: Authentication and billing flows can involve API keys, SMS codes, and payment orders.

Mitigation: Provide SMS codes or create payment orders only when intentionally using the LinkFox account or billing flow, and avoid storing API keys in shell profiles where possible.

Risk: Product research results and cached responses may remain in local linkfox output directories.

Mitigation: Inspect or clean the local linkfox output and cache directories after use, especially when handling sensitive research.

Risk: Automatic feedback reporting can expose task context or product research details.

Mitigation: Disable feedback reporting or make it opt-in before using the skill with sensitive product, account, or billing information.

## Reference(s):

- [API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-seerfar-ozon-product-detail-search)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON responses, saved JSON files, and concise Markdown-readable summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full responses are saved under a linkfox session data directory; large responses print a summary unless inline output is requested.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
