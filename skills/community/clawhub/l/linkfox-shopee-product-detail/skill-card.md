## Description:

Looks up the current public detail snapshot for one supported Shopee product URL, including available price, discount, sales, stock, SKU variants, media, brand, category, shop, and rating fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace operators, ecommerce analysts, and developers use this skill to inspect one known public Shopee listing for current pricing, inventory, variant, content, and shop signals. It is suited to listing audits and competitive page review, not keyword search, bulk screening, historical tracking, reviews, or seller-account operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a LinkFox API key and may guide users through LinkFox account or billing onboarding.

Mitigation: Install and use it only when the publisher is trusted; avoid entering phone or SMS codes through an agent unless that trust has been established.

Risk: The skill can cache or persist lookup responses locally.

Mitigation: Review the local LinkFox output directory for sensitive listing data and clean it according to the workspace retention policy.

Risk: Environment endpoint overrides can redirect API traffic outside the default LinkFox gateway.

Mitigation: Use endpoint override environment variables only in controlled development or testing environments.

Risk: The provided security verdict is suspicious because the skill combines product lookup with login, billing, feedback reporting, and broad local persistence behavior.

Mitigation: Review the skill and its network, credential, billing, feedback, and file-writing behavior before deployment.

## Reference(s):

- [Shopee 商品详情 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown summaries with optional inline JSON and saved JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-product lookup; full responses are persisted locally, with summaries printed for large responses.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
