## Description:

This skill helps agents query SellerSprite-backed Amazon competitor product data across 12 marketplaces, including sales, revenue, BSR, pricing, ratings, seller, brand, category, variation, and growth metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce analysts use this skill to discover competing products, benchmark product performance, and review market signals by ASIN, keyword, seller, brand, or category.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox API keys, phone-number based onboarding, and paid credit usage.

Mitigation: Install only when the user trusts LinkFox with this data, obtain and store the API key through the official site when possible, and confirm additional paid-credit usage before repeated calls.

Risk: Endpoint override environment variables can redirect API or onboarding requests away from the default LinkFox services.

Mitigation: Avoid setting endpoint override variables unless the destination is intentionally reviewed and trusted.

Risk: Saved output and cache files may contain Amazon research data and query results.

Mitigation: Clear local LinkFox cache and output files after use in shared environments.

Risk: Automatic feedback submission may disclose task context or user reactions to the publisher.

Mitigation: Disable or avoid automatic feedback submission when the task context is sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-sellersprite-competitor-lookup)
- [卖家精灵-查竞品 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Files, Shell commands, Guidance]

**Output Format:** [Markdown summaries and tables with saved JSON data files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved under a LinkFox session data directory; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
