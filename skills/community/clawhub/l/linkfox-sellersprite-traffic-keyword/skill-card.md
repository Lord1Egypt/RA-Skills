## Description:

Queries SellerSprite traffic keyword data for an Amazon ASIN, including keyword sources, traffic share categories, conversion categories, organic rank, ad rank, historical month filters, and sorting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace analysts, sellers, and agent users use this skill to inspect keyword traffic sources and ranking signals for a specific Amazon ASIN. It helps retrieve structured SellerSprite keyword data while preserving result files for follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts LinkFox/SellerSprite services with ASIN query data and API credentials.

Mitigation: Install and run it only when that data sharing is acceptable, and confirm destination URLs before entering credentials or running API calls.

Risk: The onboarding helper can create API keys and initiate payment-order flows.

Mitigation: Prefer obtaining keys directly from the official provider site, and use the in-skill SMS login or payment flow only after verifying the provider and payment destination.

Risk: Full API responses and cache files are persisted in local linkfox session directories.

Mitigation: Treat generated response files as sensitive when ASIN or keyword data is confidential, and review or clean the local cache and session folders after use.

Risk: Automatic feedback reporting may send skill-quality feedback to the publisher service.

Mitigation: Avoid including secrets, proprietary ASIN analysis, or customer-sensitive details when feedback content is generated or submitted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-sellersprite-traffic-keyword)
- [卖家精灵-流量词反查 API 参考](artifact/references/api.md)
- [解决认证和算力问题](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown guidance, shell commands, and JSON API responses saved to local files with summaries printed to stdout for larger responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires marketplace and ASIN inputs, can consume 15 credits per query, caches matching requests for 24 hours, and writes full responses under the local linkfox session data directory.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
