## Description:

按ASIN查找亚马逊同细分市场（Niche）竞品，支持点击转化率、综合转化率、点击量、销量、评论、评分、价格、毛利率等多维度筛选潜力竞品。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and e-commerce analysts use this skill to find same-niche competitors for a reference ASIN and compare marketplace metrics such as conversion, clicks, sales, reviews, ratings, price, fees, and gross margin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends ASIN research parameters and session metadata to LinkFox services using a LinkFox API key.

Mitigation: Use a dedicated API key with the minimum required account scope and disclose the network transfer before running competitor lookups.

Risk: Full API responses are retained in local JSON files and may contain research data or account-related session context.

Mitigation: Store outputs only in an approved workspace, review retention needs, and delete saved response files when they are no longer needed.

Risk: The onboarding helper can guide account registration, API key retrieval, plan selection, and payment order creation.

Mitigation: Require explicit user consent before registration, billing, or payment steps, and do not store API keys in shell startup files when a secret manager is available.

Risk: Automatic feedback reporting may send user sentiment or issue details to a separate LinkFox feedback endpoint.

Mitigation: Disable or avoid feedback submission unless the user has consented to the content being sent.

Risk: Environment-variable endpoint overrides can redirect credential-bearing requests away from the default LinkFox endpoints.

Mitigation: Run with trusted endpoint environment variables only, or unset endpoint override variables before use.

## Reference(s):

- [Skill listing](https://clawhub.ai/linkfox-ai/skills/linkfox-jiimore-page-asins-by-asin)
- [Publisher profile](https://clawhub.ai/user/linkfox-ai)
- [API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [LinkFox Skills](https://skill.linkfox.com/)
- [LinkFox Agent](https://agent.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance, configuration]

**Output Format:** [Markdown explanations with tables, JSON API results, saved JSON files, and shell commands for lookup or onboarding flows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The lookup script saves full API responses locally, prints small responses inline, summarizes larger responses, and uses a 24-hour local cache for repeated parameter sets.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
