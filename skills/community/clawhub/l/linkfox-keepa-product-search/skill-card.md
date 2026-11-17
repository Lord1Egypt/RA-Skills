## Description:

基于Keepa数据的亚马逊高级商品搜索与筛选，支持品类、价格、月销量、关键词、BSR排名、评论数、评分、包装尺寸、重量、配送方式等多维度条件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and ecommerce researchers use this skill to turn product-research criteria into Keepa-backed Amazon product searches, compare structured product metrics, and inspect saved JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid LinkFox Keepa gateway and may trigger account, billing, or plan-purchase flows.

Mitigation: Use it only when the user intends to spend LinkFox credits, explain additional cost before repeated searches, and require explicit approval before any plan purchase or payment order.

Risk: The skill depends on LinkFox API keys and SMS onboarding flows.

Mitigation: Avoid exposing API keys, phone numbers, or one-time passwords in shared logs; prefer a secure secret store over shell profile files where possible.

Risk: The release security summary reports silent feedback reporting plus credential and local-storage behaviors that need review before installation.

Mitigation: Review the skill before installing, run it only with trusted environment variables, and inspect generated local files before sharing the workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-keepa-product-search)
- [Keepa Product Search API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples, shell commands, and saved JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The search script saves full API responses under a linkfox session data directory and prints either full JSON or a concise summary depending on response size.]

## Skill Version(s):

1.0.7 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
