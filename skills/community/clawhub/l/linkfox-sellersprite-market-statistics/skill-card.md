## Description:

Fetches node-level Amazon category market statistics through SellerSprite, including top-listing averages, price, BSR, sales, seller counts, and new-product metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce analysts, and developers use this skill to retrieve category-level Amazon market statistics for market assessment and competition analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses LinkFox credentials and can guide phone/SMS onboarding and payment order flows.

Mitigation: Prefer manually obtaining API keys, store them in a secure secret manager, and confirm billing actions before running onboarding or order commands.

Risk: The skill writes market research responses and cache data to local session directories.

Mitigation: Review output and cache locations before use, especially when category analysis or response data is sensitive.

Risk: The skill can send feedback externally and allows endpoint override environment variables.

Mitigation: Use trusted runtimes, avoid endpoint overrides unless approved, and review when feedback reporting is appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-sellersprite-market-statistics)
- [卖家精灵-选市场统计 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses and saved JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return full JSON for small responses, a summary for larger responses, and guidance for authentication or billing issues.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
