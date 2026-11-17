## Description:

Retrieves structured 1688 product details by offer ID, including title, attributes, SKU prices and stock, logistics, supplier metrics, and procurement terms for sourcing decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and sourcing agents use this skill to inspect a known 1688 product by offer ID or product URL before quoting, supplier evaluation, logistics planning, or procurement review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LinkFox receives product IDs, lookup parameters, API keys, and selected session metadata during use.

Mitigation: Use only when that data sharing is acceptable, obtain API keys directly from the provider when possible, and verify LinkFox endpoint environment variables before running.

Risk: Authentication and billing helper commands can handle phone-based login and create payment orders.

Mitigation: Avoid login or order commands unless needed, and invoke billing/order actions only when the user intends to purchase credits.

Risk: Saved response and cache files may contain sourcing, supplier, pricing, or logistics data.

Mitigation: Review and clean up local linkfox response and cache files according to the workspace data-handling policy.

Risk: Product price, inventory, logistics, and supplier data are live and can change.

Mitigation: Use --no-cache for price-sensitive checks and confirm final purchase terms through order preview before buying.

## Reference(s):

- [1688 商品详情 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)
- [ClawHub release page](https://clawhub.ai/linkfox-ai/skills/linkfox-1688-product-detail)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown-facing summaries, stdout JSON, and saved JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes full lookup responses under a local linkfox session data directory; default cache is 24 hours unless --no-cache is used.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
